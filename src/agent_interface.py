import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from logger import logger

load_dotenv()

class AgentInterface:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY not found in .env file!")
            
        self.client = genai.Client(api_key=api_key)
        self.model_id = "models/gemini-2.5-flash-lite"
        self.system_prompt = (
            "You are a helpful, direct, and clear AI assistant. "
            "Answer questions naturally using complete sentences, but keep your responses strictly to the point. "
            "Do not overexplain, do not offer   unsolicited trivia, and provide only one best solution unless asked for more."
        )
        logger.info("🔌 Agent Interface successfully connected to the Gemini API.")

    def run_agent(self, input_text: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=input_text,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.7
                )
            )
            return response.text

        except Exception as e:
            logger.error(f"Gemini API Execution Error: {str(e)}")
            return f"Agent Execution Error: {str(e)}"
        
# -------------------------------------------------------------
# MOCK AGENT — Uncomment this class and comment out the one
# above if you want to test the framework without any API calls.
# -------------------------------------------------------------
# class AgentInterface:
#     def __init__(self):
#         logger.info("🔌 Agent Interface running in MOCK mode (no API calls).")
#
#     def run_agent(self, input_text: str) -> str:
#         return f"This is a mock response to: '{input_text}'"

# api_key = os.environ.get("GEMINI_API_KEY")

# client = genai.Client(api_key=api_key)

# print("Available Models:")
# for model in client.models.list():
#     print(f"- {model.name}")