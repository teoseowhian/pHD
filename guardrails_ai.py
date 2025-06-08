from guardrails import Guard
from guardrails.hub import ToxicLanguage
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def guardrails_ai(vAR_input):
    # Initialize the Guard with the desired validators
    guard = Guard().use(
        ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail="exception")
    )
    try:
        result = guard.validate(vAR_input)
        if result.validation_passed:
            print("Validation successful: The input is appropriate.")
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": vAR_input}
                ]
            )
            response_content = completion.choices[0].message.content
            if response_content:
                completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": vAR_input}
                ])
                print(completion.choices[0].message.content)
                return completion.choices[0].message.content
        else:
            print("Validation failed: The input contains prohibited content.")
            return "Your input contains content that violates our guidelines. Please modify and try again."
    except Exception as e:
        print(f"Validation encountered an issue: {e}")
        return "Your input contains content that violates our guidelines. Please modify and try again."
        
