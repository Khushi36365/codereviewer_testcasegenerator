from llm import client, MODEL_NAME
from prompts.analyzer import ANALYZER_PROMPT
from utils.json_parser import extract_json


def analyze_code(code: str):

    prompt = f"""
    {ANALYZER_PROMPT}

    CODE:

    ```python
    {code}
    ```
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=4000
    )

    result = response.choices[0].message.content

    try:
        return extract_json(result)

    except Exception as e:
        return {
            "error": str(e),
            "raw_output": result
        }