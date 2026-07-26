from __future__ import annotations
import json
import re
import shutil

INPUT_FILE = "interviews.jsonl"
BACKUP_FILE = "interviews_backup.jsonl"

TEXT_KEYS = (
    "description", "problem", "prompt", "question",
    "name", "input", "text", "query", "instruction"
)
PLACEHOLDER_TAGS = re.compile(r"^tag\d+$", re.IGNORECASE)


def unescape_captured(s: str) -> str:
    # Broken JSON often has literal newlines/tabs; escape them so json.loads can parse.
    repaired = re.sub(r"[\x00-\x1f]", lambda m: f"\\u{ord(m.group(0)):04x}", s)
    try:
        return json.loads(f'"{repaired}"')
    except json.JSONDecodeError:
        return s.strip()


def extract_from_dict(obj: dict) -> str | None:
    for key in TEXT_KEYS:
        val = obj.get(key)
        if isinstance(val, str) and len(val.strip()) > 15:
            return val.strip()
        if isinstance(val, list) and val and isinstance(val[0], str) and len(val[0].strip()) > 15:
            return val[0].strip()

    #last resort: any long string value
    for v in obj.values():
        if isinstance(v, str) and len(v.strip()) > 40:
            return v.strip()

def clean_question(q: str) -> str | None:
    qs = (q or "").strip()
    if not qs:
        return None

    #normal question
    if not qs.startswith("{"):
        return qs

    #valid json obj/list
    try:
        obj = json.loads(qs)
        if isinstance(obj, dict):
            return extract_from_dict(obj)
        if isinstance(obj, str) and len(obj.strip()) > 15:
            return obj.strip()
        if isinstance(obj, list) and obj and isinstance(obj[0], str):
            return obj[0].strip() if len(obj[0].strip()) > 15 else None
    except json.JSONDecodeError:
        pass
    
    #broken json, pull known fields with regex
    for key in TEXT_KEYS:
        m = re.search(rf'"{key}"\s*:\s*"((?:\\.|[^"\\])*)"', qs)
        if m and len(m.group(1).strip()) > 15:
            return unescape_captured(m.group(1))
        
    #{"Actual question text..."}
    if '":' not in qs[:60]:
        inner = qs.lstrip("{").lstrip('"').rstrip("}").rstrip('"').strip()
        if len(inner) > 20:
            return inner
        
    return None


def clean_answer(result: dict) -> str | None:
        
    answer = (result["answer"] or "").strip()

    if not answer:
        return None

    if answer.startswith(("{", "[")):
        try:
            json.loads(answer)
        except json.JSONDecodeError:
            return None

    return answer
    
def clean_tags(result: dict) -> list[str]:
    cleaned = []
    seen = set()
    tags = result.get("tags")
    
    for tag in tags:
        if not isinstance(tag, str):
            continue
        t = tag.strip()
        if not t:
            continue
        if PLACEHOLDER_TAGS.fullmatch(t):
            continue
        if t.lower() in {"tag", "tags", "n/a", "none", "null"}:
            continue
        
        key = t.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(t)
    return cleaned


shutil.copy(INPUT_FILE, BACKUP_FILE)

kept, rewritten, removed = [], 0, 0

with open(BACKUP_FILE, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        question = item.get("question")
        answer = clean_answer(item)
        tags = clean_tags(item)
        cleaned_question = clean_question(question)
        if not cleaned_question or not answer:
            removed += 1
            continue
        if cleaned_question != question:
            rewritten += 1
        item["question"] =  cleaned_question
        item["answer"] = answer
        item["tags"] = tags
        kept.append(item)
        
with open(INPUT_FILE, "w", encoding="utf-8") as f:
    for item in kept:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
        
print(f"kept={len(kept)} rewritten={rewritten} removed={removed}")