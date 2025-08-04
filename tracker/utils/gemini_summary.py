import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
print(GOOGLE_API_KEY)

client = genai.Client()

def generate_monthly_summary(data_list):
    """
    data_list = [
        {"title": "Salary", "amount": 3000, "type": "income"},
        {"title": "Groceries", "amount": 500, "type": "expense"},
        ...
    ]
    """

    prompt = (
        "Here is my monthly finance data. "
        "Give a brief summary in 100 words. Use simple language.\n\n"
    )

    for item in data_list:
        prompt += f"- {item['type'].capitalize()}: {item['title']} = {item['amount']}\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)  # optional
        )
    )
    return response.text
