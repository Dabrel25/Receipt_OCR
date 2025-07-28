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
- amount (if total amount is available on the receipt, equate it to this. Otherwise get the total sum of all items in the receipt)
- date (as ISO format: YYYY-MM-DD)

This is a normal workflow for the receipt parser. 
Given the following receipt:
 ## East Repair Inc.

RECEIPT

1912 Harvest Lane New York, NY 12210

Bill To

Ship To

Receipt #

US-001

John Smith 2 Court Square New York, NY 12210

John Smith 3787 Pineview Drive Cambridge, MA 12210

Receipt Date

11/02/2019

23122019

Due Date

26/02/2019

|   QTY | DESCRIPTION                 |   UNIT PRICE |   AMOUNT |
|-------|-----------------------------|--------------|----------|
|     1 | Front and rear brake cables |          100 |      100 |
|     2 | New set of pedal arms       |           15 |       30 |
|     3 | Labor 3hrs                  |            5 |       15 |

Subtotal

145.00

Sales Tax 6.258

TOTAL

9.06

$154.06

Terms &amp; Conditions

Payment is due within 15 days

Please make checks payable to: East Repair Inc.

This LLM will do the following steps:
1. Read through markdown and use contextual analysis to find key fields. (e.g. merchant, date, item, amount)
2. If there is no direct reference to a field, use contextual analysis to find the field. (e.g. merchant - name of company at the top of the receipt)
3. To find the amount look for keywords like total and total amount to find the sum of the items instead of individual fields.
4. If the receipt is missing a field, leave it null.
5. Return the JSON in the correct format.

Look out for any characters that might be misinterpreted such as currency symbols. Use contextual analysis to determine. (e.g. $100 as 8100, ₱2013 as P2013, etc.)

Return only: merchant, item, amount, date.
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
