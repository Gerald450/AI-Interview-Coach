import json
import re
import shutil

INPUT_FILE = "interviews.jsonl"
BACKUP_FILE = "interviews_backup.jsonl"

TEXT_KEYS = (
    "description", "problem", "prompt", "question",
    "name", "input", "text", "query", "instruction"
)

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
            return m.group(1).encode().decode("unicode_escape")
        
    #{"Actual question text..."}
    if '":' not in qs[:60]:
        inner = qs.lstrip("{").lstrip('"').rstrip("}").rstrip('"').strip()
        if len(inner) > 20:
            return inner
        
    return None

shutil.copy(INPUT_FILE, BACKUP_FILE)

kept, rewritten, removed = [], 0, 0

with open(BACKUP_FILE, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        original = item.get("question", "")
        cleaned = clean_question(original)
        if cleaned is None:
            removed += 1
            continue
        if cleaned != original:
            rewritten += 1
            item["question"] = cleaned
        kept.append(item)
        
with open(INPUT_FILE, "w", encoding="utf-8") as f:
    for item in kept:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
        
print(f"kept={len(kept)} rewritten={rewritten} removed={removed}")