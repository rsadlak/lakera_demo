import os
import openai
from dotenv import load_dotenv
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPEN_AI_KEY")

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
