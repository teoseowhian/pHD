import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from io import BytesIO

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import json
def serialize(obj):
    """Recursively walk object's hierarchy."""
    if isinstance(obj, (bool, int, float, str)):
        return obj
    elif isinstance(obj, dict):
        obj = obj.copy()
        for key in obj:
            obj[key] = serialize(obj[key])
        return obj
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize(item) for item in obj)
    elif hasattr(obj, '__dict__'):
        return serialize(obj.__dict__)
    else:
        return repr(obj)  # Don't know how to handle, convert to string

def single_openai_gradrails_text(vAR_input):
    

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=vAR_input,
    )

    output = response.results[0]
    
    # Serialize the output object
    serialized_output = serialize(output)


    # Convert the serialized output to a JSON formatted string with indentation
    json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)

    # Print the JSON string
    print(json_output)
    return json_output

def openai_gradrails_text(vAR_input):
    

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=vAR_input,
    )

    output = response.results[0]
    
    # Serialize the output object
    serialized_output = serialize(output)


    # Convert the serialized output to a JSON formatted string with indentation
    json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)

    # Print the JSON string
    print(json_output)
    
    # Parse the JSON string into a dictionary
    response_openai_dict = json.loads(json_output)
    
    if response_openai_dict["flagged"]:
        # Retrieve category scores
        category_scores = response_openai_dict["category_scores"]
        # Find the category with the highest score
        highest_category = max(category_scores, key=category_scores.get)
        highest_score = category_scores[highest_category]
        # Display the category and its score
        response_moderation = f"Content flagged due to '{highest_category}' with a score of {highest_score:.2}"
        return response_moderation
    else:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": vAR_input}
            ]
        )
        return completion.choices[0].message.content
    


def openai_gradrails_image(image_file):
    # Convert uploaded file to base64
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    image_data_url = f"data:image/jpeg;base64,{image_base64}"
    response = client.moderations.create(
    model="omni-moderation-latest",
    input=[
        {
            "type": "image_url",
            "image_url": {
                "url": image_data_url,
                # can also use base64 encoded image URLs
                # "url": "data:image/jpeg;base64,abcdefg..."
            }
        },
    ],
    )
    output = response.results[0]
    
    # Serialize the output object
    serialized_output = serialize(output)


    # Convert the serialized output to a JSON formatted string with indentation
    json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)

    # Print the JSON string
    print(json_output)
    
    # Parse the JSON string into a dictionary
    response_openai_dict = json.loads(json_output)
    
    if response_openai_dict["flagged"]:
        # Retrieve category scores
        category_scores = response_openai_dict["category_scores"]
        print(category_scores)
        # Find the category with the highest score
        highest_category = max(category_scores, key=category_scores.get)
        print(highest_category)
        highest_score = category_scores[highest_category]
        print(highest_score)
        # Display the category and its score
        response_moderation = f"Content flagged due to '{highest_category}' with a score of {highest_score:.2}"
        return response_moderation
    else:
        print("Nothing")
        response_moderation = "Nothing"
        return response_moderation



def openai_gradrails_audio(audio_file):
    
    file_name = audio_file.name.split('/')[-1]
    
    # Open the audio file as binary
    audio_binary = audio_file.read()
    
    # Write to a temporary file
    with open(file_name, "wb") as f:
        f.write(audio_binary)

    # Open the temporary file for Whisper API
    with open(file_name, "rb") as audio_for_api:
        transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_for_api
        )
    text = transcription.text
    print(text)
    
    return openai_gradrails_text(text), text
        
def openai_gradrails_video(video_file):
    # Read the image file and encode it in base64
    with open(video_file, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode('utf-8')
    response = client.moderations.create(
    model="omni-moderation-latest",
    input=[
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
            }
        },
    ],
    )
    output = response.results[0]
    
    # Serialize the output object
    serialized_output = serialize(output)


    # Convert the serialized output to a JSON formatted string with indentation
    json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)

    # Print the JSON string
    print(json_output)
    
    # Parse the JSON string into a dictionary
    response_openai_dict = json.loads(json_output)
    
    if response_openai_dict["flagged"]:
        # Retrieve category scores
        category_scores = response_openai_dict["category_scores"]
        print(category_scores)
        # Find the category with the highest score
        highest_category = max(category_scores, key=category_scores.get)
        print(highest_category)
        highest_score = category_scores[highest_category]
        print(highest_score)
        # Display the category and its score
        response_moderation = f"Content flagged due to '{highest_category}' with a score of {highest_score:.2}"
        return response_moderation
    else:
        print("Nothing")
        response_moderation = "Nothing"
        return response_moderation


# from pathlib import Path
# def openai_gradrails_video(folder_path):
#     from openai import OpenAI
#     client = OpenAI()

#     # List all images in the folder
#     frames = sorted(Path(folder_path).glob("*.jpg"))

#     # Select up to 10 images (evenly spaced if there are more than 10)
#     if len(frames) > 10:
#         step = len(frames) // 10
#         selected_frames = [frames[i] for i in range(0, len(frames), step)[:10]]
#     else:
#         selected_frames = frames
    
#     # Prepare input for moderation API
#     inputs = []
#     for frame in selected_frames:
#         inputs.append(
#             {
#                 "type": "image_url",
#                 "image_url": {
#                     # You can also encode images to base64 if needed
#                     "url": f"file://{frame.resolve()}"
#                 }
#             }
#         )
#     print(inputs)
#     # Call OpenAI moderation API
#     response = client.moderations.create(
#         model="omni-moderation-latest",
#         input=inputs
#     )
#     output = response.results[0]
    
#     # Serialize the output object
#     serialized_output = serialize(output)


#     # Convert the serialized output to a JSON formatted string with indentation
#     json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)

#     # Print the JSON string
#     print(json_output)
    
#     # Parse the JSON string into a dictionary
#     response_openai_dict = json.loads(json_output)
    
#     if response_openai_dict["flagged"]:
#         # Retrieve category scores
#         category_scores = response_openai_dict["category_scores"]
#         print(category_scores)
#         # Find the category with the highest score
#         highest_category = max(category_scores, key=category_scores.get)
#         print(highest_category)
#         highest_score = category_scores[highest_category]
#         print(highest_score)
#         # Display the category and its score
#         response_moderation = f"Content flagged due to '{highest_category}' with a score of {highest_score:.2}"
#         return response_moderation
#     else:
#         print("Nothing")
#         response_moderation = "Nothing"
#         return response_moderation
