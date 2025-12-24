import os
from openai import OpenAI

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)

def call_llm(messages: list) -> str:
    client = get_client()
    response = client.responses.create(
        model="gpt-4o-mini",
        input=messages,
        temperature=0.4,
    )
    return response.output_text
