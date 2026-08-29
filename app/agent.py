import os
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)


def generate_youtube_idea(topic):
    """
    Generates YouTube video ideas based on a topic.
    """

    prompt = f"""
    Generate 5 creative YouTube video ideas about:

    {topic}

    Make the ideas interesting, beginner-friendly, and engaging.
    Number each idea.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content