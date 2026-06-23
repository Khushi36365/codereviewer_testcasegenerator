# agents/scenario_generator.py

from llm import client
from prompts.scenarios import SCENARIO_GENERATOR_PROMPT
from utils.json_parser import extract_json


def generate_scenarios(code: str, analysis: dict):

    prompt = f"""
    {SCENARIO_GENERATOR_PROMPT}

    SOURCE CODE:

    ```python
    {code}
    ```

    ANALYSIS:

    {analysis}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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