import os
from groq import Groq
from portkey_ai import Portkey

def read_text_file(file_path):
    """Read the text from a file and return its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def initialize_portkey(api_key, virtual_key):
    """Initialize the Portkey client."""
    return Portkey(api_key=api_key, virtual_key=virtual_key)

def create_chat_completion(portkey, text):
    """Create a chat completion using the Portkey client."""
    try:
        chat_completion = portkey.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a highly skilled academic with expertise in multiple disciplines, "
                        "fluent in Turkish. Write a formal, structured project proposal in Turkish, using a clear and professional tone. "
                        "Organize the content logically with sections like introduction, objectives, methodology, and conclusions. "
                        "Use data and citations to support your points, and ensure your writing is both insightful and accessible. "
                        "Focus on critical analysis, providing evaluations and recommendations, and maintain a clear goal-oriented approach throughout the proposal."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Here is the extracted content from the .txt file:\n{text}\n  \
                    Now, based on this content, can you help me rewrite 'Proje Özeti' in Turkish and detailed."
                },
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred while creating the chat completion: {e}")
        return None

def main():
    # Read the text from a .txt file
    txt_file_path = "text.txt"
    text = read_text_file(txt_file_path)
    if text is None:
        return

    # Initialize the Groq client
    api_key = os.environ.get("GROQ_API_KEY")
    virtual_key = os.environ.get("VIRTUAL_KEY")
    if not api_key or not virtual_key:
        print("Error: API key or virtual key not found in environment variables.")
        return
    
    portkey = initialize_portkey(api_key, virtual_key)

    # Create the prompt using the text from the .txt file and the follow-up question
    response = create_chat_completion(portkey, text)
    if response:
        # Output the response
        print(response)

if __name__ == "__main__":
    main()
