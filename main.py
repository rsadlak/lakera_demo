import os
import openai
import requests
import time
from dotenv import load_dotenv
load_dotenv()

# load API keys from environment variables
openai.api_key = os.getenv("OPEN_AI_KEY")
lakera_api_key = os.getenv("LAKERA_API_KEY")
lakera_project_id = os.getenv("LAKERA_PROJECT_ID")

# Define the system role for the AI assistant for a medical device company
system_role = """
You are a helpful healthcare information assistant for medical device company.
Your role is to provide general health information and guide visitors 
to appropriate resources—NOT to provide medical advice or clinical care.
"""


def is_safe(user_prompt):
    #Check the prompt against Lakera Guard API
    session = requests.Session()

    url = "https://api.lakera.ai/v2/guard"
    payload = {"messages": [{"content": user_prompt, "role": "user"}], "project_id": lakera_project_id}
    headers = {"Authorization": f"Bearer {lakera_api_key}"}
    
    try:
        response = session.post(url, json=payload, headers=headers)
        print(f"\n LAKERA API RESPONSE TIME: {response.elapsed.total_seconds():.4f} SECONDS \n")
        result = response.json()

    except Exception as e:
        print("An error occurred while communicating with the Lakera Guard API: ", {e})
        return False, {"error": str(e)}
    
    return not result.get("flagged", False), result

def chat_session():
    #Get User input
    print("--- Welcome to the interactive OpenAI CLI! Type 'exit' to end the session. ---")

    #Initialize message history to keep context
    messages = [{"role": "system", "content": system_role}]

    #setup system role for the assistant
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
    except Exception as e:
        print("An error occurred while communicating with the OpenAI API: ", {e})
        return

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
            try:
                # Call OpenAI API to get response

                start_time = time.perf_counter()

                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )

                end_time = time.perf_counter()
                elapsed = end_time - start_time

                # Print OpenAI API response time
                print(f"OPENAI API RESPONSE TIME: {elapsed:.4f} SECONDS")
                # Extract and display the assistant's reply
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
