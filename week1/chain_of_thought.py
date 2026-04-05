import os
import re

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

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = "You are a helpful assistant. Solve the problem step by step, showing your reasoning clearly, and end with the final answer in the format 'Answer: <number>'."


USER_PROMPT = """
Solve this problem, then give the final answer on the last line as "Answer: <number>".

what is 3^{12345} (mod 100)?
"""


# For this simple example, we expect the final numeric answer only
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """Extract the final 'Answer: ...' line from a verbose reasoning trace.

    - Finds the LAST line that starts with 'Answer:' (case-insensitive)
    - Normalizes to 'Answer: <number>' when a number is present
    - Falls back to returning the matched content if no number is detected
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # Prefer a numeric normalization when possible (supports integers/decimals)
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """Run up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": USER_PROMPT},
        ]
        print("Sending messages:")
        for msg in messages:
            print(f"  {msg['role']}: {msg['content']}")
        response = client.chat.completions.create(
            model="glm-4",  # 使用 Zhipu 的模型名称
            messages=messages,
            temperature=0.3,
        )
        output_text = response.choices[0].message.content
        print(f"Response from model: {output_text}")
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
