import os

from google import genai
from google.genai import types


class GeminiClient:
    def __init__(self, api_key: str = None, model: str = "gemini-3.0-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=self.api_key)
        self.model = model

    def generate_documentation(
        self, prompt: str, system_instruction: str = None
    ) -> str:
        config = types.GenerateContentConfig(
            temperature=1.0,
            thinking_config=types.ThinkingConfig(include_thoughts=False),
        )

        if system_instruction:
            config.system_instruction = system_instruction

        try:
            response = self.client.models.generate_content(
                model=self.model, contents=prompt, config=config
            )
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API Error: {e}")
            raise e
