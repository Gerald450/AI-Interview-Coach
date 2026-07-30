import torch
from accelerate import Accelerator
from datasets import load_dataset
from rich import print
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import DataCollatorForLanguageModeling, get_scheduler
from unsloth import FastLanguageModel

accelerator = Accelerator()


def spot_check(
    model,
    tokenizer,
    dataset,
    accelerator,
    num_samples: int = 5,
    max_new_tokens: int = 256,
):
    model.eval()
    FastLanguageModel.for_inference(model)

    samples = dataset["validation"].select(
        range(min((num_samples), len(dataset["validation"])))
    )

    for i, ex in enumerate(samples):
        user_msg = ex["messages"][0]

        prompt = tokenizer.apply_chat_template(
            [user_msg], tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(prompt, return_tensors="pt").to(accelerator.device)

        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
            )

        new_tokens = output_ids[0][inputs["input_ids"].shape[-1] :]
        answer = tokenizer.decode(new_tokens, skip_special_tokens=True)

        if accelerator.is_main_process:
            print("=" * 60)
            print(f"[{i + 1}] Q: {user_msg['content'][:400]}")
            print(f"A: {answer}")
            if len(ex["messages"]) > 1:
                print(f"REF: {ex['messages'][1]['content'][:400]}")


checkpoint = "unsloth/Qwen2.5-3B-Instruct"
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=checkpoint,
    max_seq_length=2048,
    load_in_4bit=True,
)

"""
PEFT- Parameter Efficient Fine Tuning, 
LoRA - Low Rank Adaptation(adds sticky notes on parameters that need adjusting)
r- rank, how much learning is needed
target_modules are layers inside the model where sticky notes are attached
alpha - how loud the Lora changes are mixed with original weights
dropout - randomly turn off some connections during training to avoid overfitting
0 means dont do that, for smaller datasets
"""
model = FastLanguageModel.getpeft_model(
    model,
    r=16,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
    lora_alpha=16,
    lora_dropout=0,
)

# load dataset
dataset = load_dataset("shimogerald/interview-coach-dataset")
# print(dataset["train"][:4])


# tokenize dataset
def tokenize(batch):
    texts = [
        tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False,
        )
        for messages in batch["messages"]
    ]

    return tokenizer(texts)


tokenized_dataset = dataset.map(
    tokenize, batched=True, batch_size=100, remove_columns=dataset["train"].column_names
)

# setup Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# setup dataloaders
train_loader = DataLoader(
    tokenized_dataset["train"], shuffle=True, batch_size=10, collate_fn=data_collator
)

eval_loader = DataLoader(
    tokenized_dataset["validation"],
    shuffle=True,
    batch_size=10,
    collate_fn=data_collator,
)

# optimizer
optimizer = AdamW(model.parameters(), lr_rate=2e-4, weight_decay=0.01)

# use accelerator
model, optimizer, train_loader, eval_loader = accelerator.prepare(
    model, optimizer, train_loader, eval_loader
)

# lr_scheduler
num_epochs = 3
num_training_steps = num_epochs * len(train_loader)
lr_scheduler = get_scheduler(
    "cosine",
    num_training_steps=num_training_steps,
    num_warmup_steps=100,
    optimizer=optimizer,
)

lr_scheduler = accelerator.prepare(lr_scheduler)

# train loop
progress_bar = tqdm(range(num_training_steps))


model.train()

for epoch in range(num_epochs):
    for batch in train_loader:
        # forward
        output = model(**batch)
        loss = output.loss
        # backward
        accelerator.backward(loss)  # computes gradient for each trainable param
        accelerator.clip_grad_norm_(model.parameters(), max_norm=1.0)

        # optimize
        optimizer.step()
        lr_scheduler.step()
        progress_bar.update(1)
        progress_bar.set_postfix(loss=loss.item())
        optimizer.zero_grad()


# eval loop

model.eval()
total_loss = 0.0
num_batches = 0

with torch.no_grad():
    for batch in eval_loader:
        outputs = model(**batch)
        loss = outputs.loss

        total_loss += accelerator.gather(loss.detach()).mean().item()
        num_batches += 1

avg_loss = total_loss / max(num_batches, 1)
if accelerator.is_main_process:
    print(
        f"eval_loss= {avg_loss:.4f} perplexity={torch.exp(torch.tensor(avg_loss)):.2f}"
    )

spot_check(model, tokenizer, dataset, accelerator, n_samples=5)
