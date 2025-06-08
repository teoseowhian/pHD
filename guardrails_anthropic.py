
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def anthropic_model(prompt):
    """
    Generate a response from the Anthropic Claude model.
    """
    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Use the Haiku model for lower costs
        max_tokens=200,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text


def moderate_message(message):
    """
    Checks if a user-provided message contains harmful content, focusing on the top category.
    """
    # Construct the moderation prompt for Anthropic Claude
    assessment_prompt = f"""
    Analyze the following message for harmful content. Focus on detecting the most relevant category 
    and provide the top violation category along with its probability value. Categories to assess 
    include: Profanity, Hate, Insult, Toxicity, Threat, and Obscene.

    Message:
    <message>{message}</message>

    Respond with ONLY a JSON object in the format below:
    {{
        "violation": <Boolean indicating whether moderation is needed>,
        "top_category": {{
            "name": "<Category name>",
            "probability": <Probability value between 0 and 1>
        }},
        "explanation": "<Optional explanation if a violation is found>"
    }}
    """
    
    # Send the request to Anthropic Claude
    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Use the Haiku model for lower costs
        max_tokens=200,
        temperature=0,
        messages=[
            {"role": "user", "content": assessment_prompt}
        ]
    )
    
    # Extract the text content directly
    raw_content = response.content[0].text

    # Parse the JSON response from Claude
    assessment = json.loads(raw_content)
    
    # Extract details from the response
    contains_violation = assessment.get('violation', False)
    top_category = assessment.get('top_category', {})
    explanation = assessment.get('explanation', None)
    
    return contains_violation, top_category, explanation


def graudrails_anthropic(vAR_input_text):
    """
    Main function to validate the input text using content moderation.
    """
    # Moderate the user prompt
    violation, top_category, explanation = moderate_message(vAR_input_text)

    if violation:
        # Construct a meaningful message
        top_category_name = top_category.get('name', 'Unknown')
        top_category_probability = top_category.get('probability', 'N/A')
        meaningful_message = (
            f"Your input violates the {top_category_name} category with a probability of "
            f"{top_category_probability}"
        )
        print("\nModeration Results:")
        print(meaningful_message)
        return meaningful_message
    else:
        print("\nNo harmful content detected. Generating model response...")
        # Generate the model's response
        response = anthropic_model(vAR_input_text)
        print(f"Model Response: {response}")
        return response
