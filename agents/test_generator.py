from llm import client
from prompts.tests import TEST_GENERATOR_PROMPT


def generate_tests(code: str, scenarios: dict):

    prompt = f"""
    {TEST_GENERATOR_PROMPT}

    SOURCE CODE:

    ```python
    {code}
    ```

    TEST SCENARIOS:

    {scenarios}
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

    return response.choices[0].message.content