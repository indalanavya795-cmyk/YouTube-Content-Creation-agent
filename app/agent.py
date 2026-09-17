import ollama


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

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
def generate_youtube_titles(idea):
    """
    Generates YouTube titles based on a video idea.
    """

    prompt = f"""
    Generate 5 catchy YouTube titles based on this video idea:

    {idea}

    Make the titles:
    - Clear and easy to understand
    - Interesting and clickable
    - Suitable for a YouTube audience
    - Not misleading

    Number each title.
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]