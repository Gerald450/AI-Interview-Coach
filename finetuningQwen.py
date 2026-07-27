# Use a pipeline as a high-level helper
from transformers import ( 
    pipeline,
    AutoModel,
    AutoTokenizer
    )


checkpoint = "Qwen/Qwen2.5-7B-Instruct"
model = AutoModel.from_pretrained(checkpoint)





pipe = pipeline("text-generation", model="Qwen/Qwen2.5-7B-Instruct")
messages = [
    {"role": "user", "content": "What is a Transformer?"},
]
pipe(messages)


