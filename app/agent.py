import os
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
def generate_youtube_description(idea):
    """
    Generates a YouTube video description based on a video idea.
    """

    prompt = f"""
    Write an engaging YouTube video description for this video idea:

    {idea}

    The description should:
    - Clearly explain what the video is about
    - Be friendly and engaging
    - Include relevant keywords naturally
    - Encourage viewers to watch
    - Be suitable for YouTube

    Keep it concise.
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
def generate_youtube_hashtags(idea):
    """
    Generates relevant YouTube hashtags based on a video idea.
    """

    prompt = f"""
    Generate 10 relevant YouTube hashtags for this video idea:

    {idea}

    Rules:
    - Make them relevant to the topic
    - Keep them short and useful
    - Do not use spaces inside a hashtag
    - Do not number them
    - Put each hashtag on a separate line
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
def generate_youtube_script(idea):
    """
    Generates a complete YouTube video script based on a video idea.
    """

    prompt = f"""
    Write a complete YouTube video script based on this idea:

    {idea}

    The script should include:
    - A strong opening hook
    - A short introduction
    - Clear main sections
    - Natural transitions
    - A friendly and engaging tone
    - A conclusion
    - A simple call to action asking viewers to like, subscribe, and comment

    Make the script suitable for a beginner-friendly YouTube video.
    Do not include camera directions or complicated production instructions.
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
def save_youtube_content(idea, titles, description, hashtags, script, thumbnail_ideas):
    """
    Saves generated YouTube content into a text file.
    """

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/youtube_content.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("YOUTUBE CONTENT CREATION AGENT\n")
        file.write("=" * 40 + "\n\n")

        file.write("VIDEO IDEA\n")
        file.write("-" * 20 + "\n")
        file.write(idea + "\n\n")

        file.write("YOUTUBE TITLES\n")
        file.write("-" * 20 + "\n")
        file.write(titles + "\n\n")

        file.write("DESCRIPTION\n")
        file.write("-" * 20 + "\n")
        file.write(description + "\n\n")

        file.write("HASHTAGS\n")
        file.write("-" * 20 + "\n")
        file.write(hashtags + "\n\n")

        file.write("VIDEO SCRIPT\n")
        file.write("-" * 20 + "\n")
        file.write(script + "\n")
        file.write("\nTHUMBNAIL IDEAS\n")
        file.write("-" * 20 + "\n")
        file.write(thumbnail_ideas + "\n")

    return file_path
    """
    Generates YouTube thumbnail ideas based on a video idea.
    """

    prompt = f"""
    Generate 5 creative YouTube thumbnail ideas for this video:

    {idea}

    Each thumbnail idea should include:
    - Main visual
    - Short text to display on the thumbnail
    - Overall concept

    Make them simple, eye-catching, and suitable for YouTube.
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
def generate_thumbnail_ideas(idea):
    """
    Generates YouTube thumbnail ideas based on a video idea.
    """

    prompt = f"""
    Generate 5 creative YouTube thumbnail ideas for this video:

    {idea}

    Each thumbnail idea should include:
    - Main visual
    - Short text to display on the thumbnail
    - Overall concept

    Make them simple, eye-catching, and suitable for YouTube.
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