import os
import openai
import requests
from dotenv import load_dotenv
load_dotenv()

# load API keys from environment variables
openai.api_key = os.getenv("OPEN_AI_KEY")
lakera_api_key = os.getenv("LAKERA_API_KEY")
lakera_project_id = os.getenv("LAKERA_PROJECT_ID")


def is_safe(user_prompt):
    #Check the prompt against Lakera Guard API
    session = requests.Session()

    url = "https://api.lakera.ai/v2/guard"
    payload = {"messages": [{"content": user_prompt, "role": "user"}], "project_id": lakera_project_id}
    headers = {"Authorization": f"Bearer {lakera_api_key}"}

    response = session.post(url, json=payload, headers=headers)
    
    result = response.json()

    return not result.get("flagged", False), result

def chat_session():
    #Get User input
    print("--- Welcome to the interactive OpenAI CLI! Type 'exit' to end the session. ---")

    #Initialize message history to keep context
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        #Get user input
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Ending chat session. Goodbye!")
            break
        
        # Append user message to history
        messages.append({"role": "user", "content": user_input})

        safe, details = is_safe(user_input)

        if not safe:
            print("\nYour input was flagged by Lakera Guard and cannot be processed. Please try again with a different prompt.")
            print("Lakera Guard details: ", details)
        else:
            print("Lakera Guard details: ", details)
            try:
                # Call OpenAI API to get response
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )
                
                # Extract and display the asssistant's reply
                assitant_reply = response.choices[0].message.content
                print("AI: " + assitant_reply)

                messages.append({"role": "assistant", "content": assitant_reply})

            except Exception as e:
                print("An error occurred while communicating with the OpenAI API: ", {e})
                break

def main():
    print("Hello from lakera-demo!\n")
    chat_session()

if __name__ == "__main__":
    main()
