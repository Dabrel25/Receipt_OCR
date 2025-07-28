from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_receipt_with_gpt(text: str) -> dict:
    prompt = f"""
You are a receipt parser. Extract these fields from the text below:

- merchant
- item 
- total amount (total sum of all items)
- date (as ISO format: YYYY-MM-DD)

Return as JSON. Do not guess values not in the text.

Receipt:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ GPT returned invalid JSON:\n", content)
        return {
            "merchant": None,
            "date": None,
            "item": None,
            "amount": None
        }
