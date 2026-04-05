from __future__ import annotations

import json
import logging
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from ..config import get_settings

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize OpenAI client (optional for testing)
client: OpenAI | None = None
settings = get_settings()
ZHIPU_API_KEY = settings.zhipu_api_key or os.environ.get("ZHIPU_API_KEY")

if ZHIPU_API_KEY:
    client = OpenAI(api_key=ZHIPU_API_KEY, base_url="https://open.bigmodel.cn/api/paas/v4/")
else:
    logger.warning("ZHIPU_API_KEY not set, LLM extraction will not be available")

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


def extract_action_items(text: str) -> list[str]:
    """Extract action items from text using heuristic pattern matching.

    Args:
        text: Note text to extract action items from.

    Returns:
        List[str]: List of extracted action item strings.
    """
    logger.debug(f"Extracting action items using heuristics from text of length {len(text)}")
    lines = text.splitlines()
    extracted: list[str] = []
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
    unique: list[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    logger.info(f"Extracted {len(unique)} action items using heuristics")
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


def _parse_json_array(text: str) -> list[str]:
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


def extract_action_items_llm(text: str) -> list[str]:
    """Use a Zhipu model to extract action items from note text.

    Args:
        text: Note text to extract action items from.

    Returns:
        List[str]: List of extracted action item strings.
    """
    if not text.strip():
        logger.debug("Empty text provided for LLM extraction")
        return []

    if client is None:
        logger.warning("LLM client not available, falling back to heuristics")
        return extract_action_items(text)

    logger.info(f"Extracting action items using LLM from text of length {len(text)}")
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

    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=messages,
            temperature=0.0,
        )
        output_text = response.choices[0].message.content
        logger.debug(f"LLM response: {output_text[:100]}...")
        items = _parse_json_array(output_text)
        if items:
            logger.info(f"LLM extraction successful: {len(items)} action items")
            return items

        # Fallback: use heuristic extraction if model output is not valid JSON.
        logger.warning("LLM output was not valid JSON, falling back to heuristics")
        return extract_action_items(text)
    except Exception as e:
        logger.error(f"LLM extraction failed: {e}")
        logger.info("Falling back to heuristic extraction")
        return extract_action_items(text)
