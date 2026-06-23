import json
import re


def extract_json(text: str):

    # JSON code block
    match = re.search(
        r"```json\s*(.*?)\s*```",
        text,
        re.DOTALL
    )

    if match:
        return json.loads(match.group(1))

    # First JSON object fallback
    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:
        return json.loads(match.group())

    raise ValueError("No valid JSON found")