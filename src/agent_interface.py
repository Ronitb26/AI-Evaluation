import os
import google.genai as genai
from dotenv import load_dotenv
from logger import logger

load_dotenv()

class AgentInterface:
    def __init__(self):
        """
        Initializes the live Gemini model as the active agent being tested.
        """
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY not found in .env file!")
            
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="You are a helpful, accurate, and safe AI assistant."
        )
        
        logger.info("🔌 Agent Interface successfully connected to Gemini API.")

    def run_agent(self, input_text: str) -> str:
        """
        Sends the test prompt directly to Gemini, waits for it to generate 
        an answer, and returns the live text back to the test runner.
        """
        try:
            response = self.model.generate_content(input_text)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Execution Error: {str(e)}")
            return f"Agent Execution Error: {str(e)}"