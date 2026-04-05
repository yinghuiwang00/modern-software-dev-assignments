import os
import re
from typing import Callable, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 获取 Zhipu API Key
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY")
if not ZHIPU_API_KEY:
    raise ValueError("ZHIPU_API_KEY environment variable is not set")

# 初始化 Zhipu API 客户端
client = OpenAI(api_key=ZHIPU_API_KEY, base_url="https://open.bigmodel.cn/api/paas/v4/")

NUM_RUNS_TIMES = 5

DATA_FILES: List[str] = [
    os.path.join(os.path.dirname(__file__), "data", "api_docs.txt"),
]


def load_corpus_from_files(paths: List[str]) -> List[str]:
    corpus: List[str] = []
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    corpus.append(f.read())
            except Exception as exc:
                corpus.append(f"[load_error] {p}: {exc}")
        else:
            corpus.append(f"[missing_file] {p}")
    return corpus


# Load corpus from external files (simple API docs). If missing, fall back to inline snippet
CORPUS: List[str] = load_corpus_from_files(DATA_FILES)

QUESTION = (
    "Write a Python function `fetch_user_name(user_id: str, api_key: str) -> str` that calls the documented API "
    "to fetch a user by id and returns only the user's name as a string."
)


YOUR_SYSTEM_PROMPT = (
    "You are a helpful coding assistant. Use ONLY the provided context to write the required function. "
    "Generate a single fenced Python code block containing imports and the function definition. "
    "Use the documented Base URL and endpoint, send the X-API-Key header, raise an exception for non-200 responses, "
    "and return only the user's name string."
)


# For this simple example
# For this coding task, validate by required snippets rather than exact string
REQUIRED_SNIPPETS = [
    "def fetch_user_name(",
    "requests.get",
    "/users/",
    "X-API-Key",
    "return",
]


def YOUR_CONTEXT_PROVIDER(corpus: List[str]) -> List[str]:
    """Select and return the relevant subset of documents from CORPUS for this task."""
    if not corpus:
        return []
    doc = corpus[0]
    if doc.startswith("[missing_file]") or doc.startswith("[load_error]"):
        return []
    return [doc]


def make_user_prompt(question: str, context_docs: List[str]) -> str:
    if context_docs:
        context_block = "\n".join(f"- {d}" for d in context_docs)
    else:
        context_block = "(no context provided)"
    return (
        f"Context (use ONLY this information):\n{context_block}\n\n"
        f"Task: {question}\n\n"
        "Requirements:\n"
        "- Use the documented Base URL and endpoint.\n"
        "- Send the documented authentication header.\n"
        "- Raise for non-200 responses.\n"
        "- Return only the user's name string.\n\n"
        "Output: A single fenced Python code block with the function and necessary imports.\n"
    )


def extract_code_block(text: str) -> str:
    """Extract the last fenced Python code block, or any fenced code block, else return text."""
    # Try ```python ... ``` first
    m = re.findall(r"```python\n([\s\S]*?)```", text, flags=re.IGNORECASE)
    if m:
        return m[-1].strip()
    # Fallback to any fenced code block
    m = re.findall(r"```\n([\s\S]*?)```", text)
    if m:
        return m[-1].strip()
    return text.strip()


def test_your_prompt(
    system_prompt: str, context_provider: Callable[[List[str]], List[str]]
) -> bool:
    """Run up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT."""
    context_docs = context_provider(CORPUS)
    user_prompt = make_user_prompt(QUESTION, context_docs)

    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        print("Sending messages:")
        for msg in messages:
            print(f"  {msg['role']}: {msg['content']}")
        response = client.chat.completions.create(
            model="glm-4",  # 使用 Zhipu 的模型名称
            messages=messages,
            temperature=0.0,
        )
        output_text = response.choices[0].message.content
        print(f"Response from model: {output_text}")
        code = extract_code_block(output_text)
        missing = [s for s in REQUIRED_SNIPPETS if s not in code]
        if not missing:
            print(output_text)
            print("SUCCESS")
            return True
        else:
            print("Missing required snippets:")
            for s in missing:
                print(f"  - {s}")
            print("Generated code:\n" + code)
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT, YOUR_CONTEXT_PROVIDER)
