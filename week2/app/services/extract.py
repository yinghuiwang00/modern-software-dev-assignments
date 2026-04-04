from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY")
if not ZHIPU_API_KEY:
    raise ValueError("ZHIPU_API_KEY environment variable is not set")

client = OpenAI(api_key=ZHIPU_API_KEY, base_url="https://open.bigmodel.cn/api/paas/v4/")

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def _parse_json_array(text: str) -> List[str]:
    json_text = text.strip()
    if json_text.startswith("```") and json_text.endswith("```"):
        json_text = json_text.strip("`")
        if json_text.lower().startswith("json\n"):
            json_text = json_text[5:]
    try:
        data = json.loads(json_text)
        if isinstance(data, list) and all(isinstance(item, str) for item in data):
            return [item.strip() for item in data if item.strip()]
    except json.JSONDecodeError:
        pass
    return []


def extract_action_items_llm(text: str) -> List[str]:
    """Use a Zhipu model to extract action items from note text."""
    if not text.strip():
        return []

    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that extracts action items from meeting notes. "
                "Respond with a JSON array of action item strings only, without extra text."
            ),
        },
        {
            "role": "user",
            "content": (
                "Extract action items from the following note text as a JSON array of strings. "
                "Use concise action item wording and do not include any explanation.\n\n"
                f"Note text:\n{text}"
            ),
        },
    ]

    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        temperature=0.0,
    )
    output_text = response.choices[0].message.content
    items = _parse_json_array(output_text)
    if items:
        return items

    # Fallback: use heuristic extraction if model output is not valid JSON.
    return extract_action_items(text)
