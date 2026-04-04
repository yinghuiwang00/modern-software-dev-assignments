import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 获取 DeepSeek API Key
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

# 初始化 DeepSeek API 客户端
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = "You are a helpful assistant. When asked to reverse the order of letters in a word, output only the reversed word without any additional text or explanation."

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

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
            model="deepseek-chat",  # 使用 DeepSeek 的模型名称
            messages=messages,
            temperature=0.5,
        )
        output_text = response.choices[0].message.content.strip()
        print(f"Response from model: {output_text}")
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)