import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def call_llm(prompt: str, system_prompt: str) -> str:
    """
    Calls the LLM with a specific prompt and system prompt.
    """
    api_key = os.getenv("API_KEY")
    api_base = os.getenv("API_BASE")

    if not api_key:
        raise ValueError("API_KEY not found in environment variables.")
    if not api_base:
        raise ValueError("API_BASE not found in environment variables.")

    client = OpenAI(api_key=api_key, base_url=api_base)
    
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred while calling the LLM: {e}")
        return "Error: Could not get a response from the model."

if __name__ == '__main__':
    # Example usage for testing
    test_system_prompt = "You are a helpful assistant."
    test_prompt = "What is the meaning of life?"
    
    print(f"System Prompt: {test_system_prompt}")
    print(f"User Prompt: {test_prompt}")
    print("-" * 20)
    
    response = call_llm(test_prompt, test_system_prompt)
    print(f"LLM Response: {response}")
