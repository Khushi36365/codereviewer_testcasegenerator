# utils/code_parser.py

def extract_python_code(text: str):

    text = text.replace("```python", "")
    text = text.replace("```", "")

    return text.strip()
