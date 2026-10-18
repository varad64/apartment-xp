import base64
import os
import json
from model import BillExtractionSchema
from openai import AsyncOpenAI
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

ai_client = AsyncOpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
    api_key="ollama",
)

async def parse_bill_gemma(image_bytes: bytes, filename: str, expected_category: str) -> Decimal:
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    prompt = f"""
    You are an automated invoice parsing engine. Analyze this image of a utility bill or maintenance receipt.
    The expected category is: {expected_category}.
    Identify and extract the total bill amount due.
    Return your output strictly conforming to the requested schema.
    
    CRITICAL INSTRUCTIONS:
    - Return only the numeric value for 'total_amount'
    - DO NOT INCLUDE currency symbols like $, Rs, or commas
    - Example: return 31152.00 instead of "$31,152"
    """

    try:
        response = await ai_client.chat.completions.create(
            model="gemma3:4b",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ]
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "bill_extraction",
                    "schema": BillExtractionSchema.model_json_schema(),
                }
            },
            temperature=0.0,
        )

        raw_json = response.choices[0].message.content
        parsed = BillExtractionSchema.model_validate_json(raw_json)
        return parsed.total_amount
    except Exception as e:
        raise ValueError(f"Gemma failed to parse the bill: {str(e)}")
