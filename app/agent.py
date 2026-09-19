import os
import base64
import requests
import ollama


# ============================================================
# YOUTUBE VIDEO IDEA GENERATOR
# ============================================================

def generate_youtube_idea(topic):
    """
    Generates YouTube video ideas based on a topic.
    """

    prompt = f"""
Generate 5 creative YouTube video ideas about:

{topic}

Make the ideas:
- Interesting
- Beginner-friendly
- Engaging
- Suitable for YouTube

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


# ============================================================
# YOUTUBE TITLE GENERATOR
# ============================================================

def generate_youtube_titles(idea):
    """
    Generates YouTube titles based on a video idea.
    """

    prompt = f"""
Generate 5 catchy YouTube titles based on this video idea:

{idea}

Make the titles:
- Clear
- Easy to understand
- Interesting
- Clickable
- Suitable for YouTube
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


# ============================================================
# YOUTUBE DESCRIPTION GENERATOR
# ============================================================

def generate_youtube_description(idea):
    """
    Generates a YouTube video description.
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


# ============================================================
# YOUTUBE HASHTAG GENERATOR
# ============================================================

def generate_youtube_hashtags(idea):
    """
    Generates relevant YouTube hashtags.
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


# ============================================================
# YOUTUBE KEYWORD GENERATOR
# ============================================================

def generate_youtube_keywords(idea):
    """
    Generates YouTube keywords/tags.
    """

    prompt = f"""
Generate 15 relevant YouTube keywords/tags for this video idea:

{idea}

Rules:
- Make them highly relevant to the topic
- Use short phrases
- Do not use hashtags
- Do not number them
- Put each keyword on a separate line
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


# ============================================================
# YOUTUBE SCRIPT GENERATOR
# ============================================================

def generate_youtube_script(idea):
    """
    Generates a complete YouTube video script.
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
- A simple call to action asking viewers to like,
  subscribe, and comment

Make the script suitable for a beginner-friendly
YouTube video.

Do not include camera directions or complicated
production instructions.
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


# ============================================================
# THUMBNAIL IDEA GENERATOR
# ============================================================

def generate_thumbnail_ideas(idea):
    """
    Generates creative YouTube thumbnail ideas.
    """

    prompt = f"""
Generate 5 creative YouTube thumbnail ideas for this video:

{idea}

Each thumbnail idea should include:
- Main visual
- Short text to display on the thumbnail
- Overall concept

Make them:
- Simple
- Eye-catching
- Professional
- Suitable for YouTube

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


# ============================================================
# ACTUAL THUMBNAIL IMAGE GENERATOR
# ============================================================

def generate_thumbnail_image(idea):
    """
    Generates a topic-specific YouTube thumbnail using
    Llama 3.2 + Draw Things.
    """

    prompt_request = f"""
Create a detailed image-generation prompt for a YouTube thumbnail
based on this video idea:

{idea}

The image prompt must describe:
- The main subject related directly to the video topic
- Important objects related to the topic
- A realistic environment
- Professional photography
- Natural realistic lighting
- Strong visual focus
- Clear composition suitable for YouTube
- A visually interesting scene
- Space for adding text later

Make the result photorealistic and specific.
Do not ask the image generator to create text or words.
Return only the image-generation prompt.
"""

    prompt_response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt_request
            }
        ]
    )

    image_prompt = prompt_response["message"]["content"]

    response = requests.post(
        "http://127.0.0.1:7860/sdapi/v1/txt2img",
        json={
            "prompt": image_prompt,
            "negative_prompt": (
                "cartoon, anime, illustration, painting, digital art, "
                "CGI, 3D render, fantasy, unrealistic, distorted, "
                "deformed, blurry, low quality, text, letters, words, "
                "watermark, logo"
            ),
            "width": 768,
            "height": 432,
            "steps": 12,
            "batch_size": 1
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    if "images" not in data or not data["images"]:
        raise RuntimeError(
            "Draw Things did not return an image."
        )

    image_data = base64.b64decode(data["images"][0])

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/thumbnail.png"

    with open(file_path, "wb") as file:
        file.write(image_data)

    return file_path

# ============================================================
# SAVE ALL GENERATED CONTENT
# ============================================================

def save_youtube_content(
    idea,
    titles,
    description,
    hashtags,
    keywords,
    script,
    thumbnail_ideas
):
    """
    Saves all generated YouTube content into a text file.
    """

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/youtube_content.txt"

    with open(file_path, "w", encoding="utf-8") as file:

        file.write(
            "YOUTUBE CONTENT CREATION AGENT\n"
        )

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

        file.write("YOUTUBE KEYWORDS\n")
        file.write("-" * 20 + "\n")
        file.write(keywords + "\n\n")

        file.write("VIDEO SCRIPT\n")
        file.write("-" * 20 + "\n")
        file.write(script + "\n\n")

        file.write("THUMBNAIL IDEAS\n")
        file.write("-" * 20 + "\n")
        file.write(thumbnail_ideas + "\n")

    return file_path