# Code Review & Test Case Generator

An AI-powered agent that reviews source code, analyzes logic, and automatically generates test scenarios and pytest test cases using Groq LLMs.

## Run

### Install dependencies

```bash
uv sync
```

### Configure environment

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

### Start the application

```bash
uv run main.py
```

Choose one of the available input methods:

1. Paste code
2. Read a file
3. Analyze an entire project folder

Generated outputs are saved inside the `output/` directory.
