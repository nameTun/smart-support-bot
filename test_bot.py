import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is not set.")
        return

    client = OpenAI(api_key=api_key)

    project_root = os.path.dirname(__file__)
    state_path = os.path.join(project_root, "sync_state.json")
    
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    vector_store_id = state.get("_global_", {}).get("vector_store_id")
    if not vector_store_id:
        print("No Vector Store found. Please run main.py first.")
        return

    print(f"Using Vector Store: {vector_store_id}")
    print("Asking question via Responses API...")
    
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input="You are OptiBot. How do I add a YouTube video?",
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vector_store_id]
            }]
        )

        print("\n========== OPTIBOT RESPONSE ==========\n")
        # Try to print output text safely depending on object structure
        if hasattr(response, 'output_text'):
            print(response.output_text)
        elif hasattr(response, 'choices'):
            print(response.choices[0].message.content)
        else:
            print(response)
        print("\n========================================\n")
        
    except Exception as e:
        print("\n[Error OPENAI]")
        print(f"Reason: {str(e)}")

if __name__ == "__main__":
    main()
