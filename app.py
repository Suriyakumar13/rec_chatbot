import openai
import gradio
import json

openai.api_key = "apikey"

# Load responses from a JSON file and convert keys to lowercase
with open("responses.json", "r") as file:
    responses = {key.lower(): value for key, value in json.load(file).items()}

# Initialize messages with the initial system message
messages = [
    {
        "role": "system",
        "content": "you are a marketing head of rajalakshmi engineering college, you will help people to know more about rajalakshmi engineering college.",
    }
]


def load_keyword_links():
    with open("responses.json", "r") as file:
        keyword_links = json.load(file)
    return keyword_links


def find_links(input_text, keyword_links):
    # Initialize a list to store found links
    found_links = []

    # Convert input text to lowercase for case-insensitive matching
    input_text_lower = input_text.lower()

    # Check input text for keywords and find associated links
    for keyword, link in keyword_links.items():
        if keyword.lower() in input_text_lower:
            found_links.append(link)

    return found_links


def CustomChatGPT(user_input):
    # Append user input to the messages
    messages.append({"role": "user", "content": user_input})

    # Find links based on user input using the terminal chatbot logic
    keyword_links = load_keyword_links()
    links = find_links(user_input, keyword_links)

    # Get response from the JSON file or the AI model
    if links:
        # If relevant links are found based on keywords, use them as the response
        links_response = "Found relevant links:\n" + "\n".join(
            [f"<br><a href='{link}'>{link}</a>" for link in links]
        )
    else:
        links_response = "<br>No relevant links found.<br>"

    if user_input.lower() in responses:
        # If the user input matches a key in the responses JSON file, use the corresponding value as the response
        ai_response = responses[user_input.lower()]
    else:
        # Otherwise, use the AI model to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        ai_response = response["choices"][0]["message"]["content"]

    # Append assistant response to the messages
    messages.append({"role": "assistant", "content": ai_response})

    # Return both the relevant links response and the AI-generated response
    return f"{links_response}\n<br>AI Response:<br>\n{ai_response}"


demo = gradio.Interface(
    fn=CustomChatGPT, inputs="text", outputs="html", title="REC bot"
)

demo.launch(share=False)
