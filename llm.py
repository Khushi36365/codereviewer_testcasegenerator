import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gpt-5-mini"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)