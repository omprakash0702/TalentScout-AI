import os
import time
from openai import OpenAI


# ---------------------------
# CLIENT
# ---------------------------
def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI(api_key=api_key)


# ---------------------------
# CLEAN RESPONSE
# ---------------------------
def clean_output(text: str) -> str:
    if not text:
        return ""

    # remove unwanted prefixes
    text = text.strip()
    text = text.replace("```json", "").replace("```", "")

    return text.strip()


# ---------------------------
# MAIN LLM CALL (STABLE)
# ---------------------------
def call_llm(messages: list, temperature=0.3, retries=3) -> str:

    client = get_client()

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=temperature,
                max_tokens=800,
            )

            content = response.choices[0].message.content

            return clean_output(content)

        except Exception as e:
            if attempt == retries - 1:
                return "⚠️ LLM error. Please try again."

            time.sleep(1)  # retry delay

    return "⚠️ Unexpected error"