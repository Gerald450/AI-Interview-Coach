from __future__ import annotations

import json
import re
from pathlib import Path

from app.models.interview import InterviewExample

TEXT_KEYS = (
    "description",
    "problem",
    "prompt",
    "question",
    "name",
    "input",
    "text",
    "query",
    "instruction",
)
PLACEHOLDER_TAGS = re.compile(r"^tag\d+$", re.IGNORECASE)


def _normalize_question(q: str) -> str:
    return "".join(q.lower().split())


class JSONLWriter:
    def __init__(self, output_path: str) -> None:
        self.output_path = Path(output_path)
        # if directory dont exist, create it, if it does dont throw error
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._seen = self._load_seen()

    def _load_seen(self) -> set[str]:
        seen: set[str] = set[str]()
        if not self.output_path.exists():
            return seen
        with self.output_path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                q = item.get("question")
                if isinstance(q, str) and q.strip():
                    seen.add(_normalize_question(q))
        return seen

    def write(self, interview: InterviewExample) -> bool:

        result = interview.model_dump(
            mode="json"
        )  # model_dump: dict, mode: json friendly
        question = self.clean_question(result)
        answer = self.clean_answer(result)

        if not question or not answer:
            return False
        key = _normalize_question(question)

        if key in self._seen:
            print(f"duplicate skipped: {question[:80]!r}")
            return False

        result["question"] = question
        result["answer"] = answer
        result["tags"] = self.clean_tags(result)

        with self.output_path.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(result, ensure_ascii=False) + "\n"  # dumps: json string,
            )
        self._seen.add(key)
        return True

    def clean_question(self, result: dict) -> dict | None:
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
                if (
                    isinstance(val, list)
                    and val
                    and isinstance(val[0], str)
                    and len(val[0].strip()) > 15
                ):
                    return val[0].strip()

            # last resort: any long string value
            for v in obj.values():
                if isinstance(v, str) and len(v.strip()) > 40:
                    return v.strip()

        def clean_question(q: str) -> str | None:
            qs = (q or "").strip()
            if not qs:
                return None

            # normal question
            if not qs.startswith("{"):
                return qs

            # valid json obj/list
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

            # broken json, pull known fields with regex
            for key in TEXT_KEYS:
                m = re.search(rf'"{key}"\s*:\s*"((?:\\.|[^"\\])*)"', qs)
                if m and len(m.group(1).strip()) > 15:
                    return unescape_captured(m.group(1))

            # {"Actual question text..."}
            if '":' not in qs[:60]:
                inner = qs.lstrip("{").lstrip('"').rstrip("}").rstrip('"').strip()
                if len(inner) > 20:
                    return inner

            return None

        cleaned = clean_question(result["question"])
        if cleaned:
            return cleaned
        else:
            print(f"Cannot clean {result['question']}")
            return None

    def clean_answer(self, result: dict) -> str | None:

        answer = (result["answer"] or "").strip()

        if not answer:
            return None

        if answer.startswith(("{", "[")):
            try:
                json.loads(answer)
            except json.JSONDecodeError:
                print(f"failed to clean answer: {answer}")
                return None

        return answer

    def clean_tags(self, result: dict) -> list[str]:
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
