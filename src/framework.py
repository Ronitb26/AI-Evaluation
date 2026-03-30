from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def run_agent(input: str) -> str:
    response = llm.invoke(input)
    return response.content

# Quick test to make sure your API key and setup are working
if __name__ == "__main__":
    test_case = "Explain how AI works in a few words"
    print("Agent Response:", run_agent(test_case))