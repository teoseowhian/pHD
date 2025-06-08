
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define the model generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model with specific system instructions for moderation
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are a content moderation assistant. Analyze user input to detect harmful content "
        "across the following categories: Profanity, Hate, Insult, Toxicity, Threat, and Obscene "
        "language. If harmful content is detected, respond with only the top category and its "
        "probability value. If no harmful content is detected, respond to the input normally."
    ),
)

# Few-shot examples for content moderation
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["I WILL KILL YOU"],
        },
        {
            "role": "assistant",
            "parts": ["Detected harmful content:\nCategory: Threat\nProbability: 0.98"],
        },
        {
            "role": "user",
            "parts": ["You are the worst assistant."],
        },
        {
            "role": "assistant",
            "parts": ["Detected harmful content:\nCategory: Insult\nProbability: 0.85"],
        },
        {
            "role": "user",
            "parts": ["Hello, how are you?"],
        },
        {
            "role": "assistant",
            "parts": ["Hello! I'm here to assist you. How can I help?"],
        },
    ]
)

# Function to process a new input
def moderate_and_respond(input_text):
    response = chat_session.send_message(input_text)
    return response.text


def image_with_gemini(input_image):
    # Configure Gemini API key
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    def upload_to_gemini(file_data, mime_type):
        """
        Uploads the given file data to Gemini.

        Parameters:
            file_data: Binary file data.
            mime_type: MIME type of the file.

        Returns:
            The uploaded file object from Gemini.
        """
        file = genai.upload_file(file_data, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    # Validate input_image
    if not hasattr(input_image, 'type'):
        raise ValueError("The input image must have a 'type' attribute for MIME type.")

    # Upload the image to Gemini
    gemini_file = upload_to_gemini(input_image, mime_type=input_image.type)

    # Configure the generative model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction=(
            "You are a content moderation assistant. Analyze user input to detect harmful content "
            "across the following categories: Profanity, Hate, Insult, Toxicity, Threat, and Obscene "
            "language. If harmful content is detected, respond with only the top category and its "
            "probability value. If no harmful content is detected, respond to the input normally."
        ),
    )

    # Start a chat session with the uploaded file
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    gemini_file,
                ],
            },
        ]
    )

    # Send a message to the model to process the image
    response = chat_session.send_message("Please analyze this attachements.")
    
    print(chat_session)
    print(response.text)
    # Return the response text
    return response.text


import os
import google.generativeai as genai

def video_with_gemini(input_video):

    # Configure the Gemini API key
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    def upload_to_gemini(file_data, mime_type):
        file = genai.upload_file(file_data, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    # Validate input_video
    if not hasattr(input_video, 'type'):
        raise ValueError("The input video must have a 'type' attribute for MIME type.")

    # Upload the video to Gemini
    gemini_file = upload_to_gemini(input_video, mime_type=input_video.type)

    # Wait for the file to become active
    def wait_for_file_to_be_active(gemini_file):
        import time
        file = genai.get_file(gemini_file.name)
        while file.state.name == "PROCESSING":
            print("File is processing, waiting for it to become active...")
            time.sleep(10)
            file = genai.get_file(gemini_file.name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process.")
        print("File is now active and ready to use.")

    wait_for_file_to_be_active(gemini_file)

    # Configure the generative model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction=(
            "You are a content moderation assistant. Analyze user input to detect harmful content "
            "across the following categories: Profanity, Hate, Insult, Toxicity, Threat, and Obscene "
            "language. If harmful content is detected, respond with only the top category and its "
            "probability value. If no harmful content is detected, respond to the input normally."
        ),
    )

    # Start a chat session with the uploaded video
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    gemini_file,
                ],
            },
        ]
    )

    # Send a message to the model to process the video
    response = chat_session.send_message("Please analyze the attached video.")

    # Print and return the response text
    print(response.text)
    return response.text
