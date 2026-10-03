import json
import re
from typing import Any

import ollama
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama3.2"


# ============================================================
# AI CORE
# ============================================================

def ask_ai(prompt: str) -> str:
    """
    Send a prompt to Ollama and return clean text.
    """

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"].strip()

    except Exception as error:
        raise RuntimeError(
            f"Ollama could not generate content: {error}"
        )


def ask_ai_json(prompt: str) -> dict[str, Any]:
    """
    Ask Ollama for JSON and safely parse the response.
    """

    response = ask_ai(prompt)

    # Remove markdown code fences if the model adds them.
    response = response.strip()

    response = re.sub(
        r"^```(?:json)?",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = re.sub(
        r"```$",
        "",
        response,
    )

    response = response.strip()

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        # Try extracting the first JSON object.
        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:
            try:
                return json.loads(
                    response[start:end + 1]
                )
            except json.JSONDecodeError:
                pass

        raise RuntimeError(
            "AI returned invalid JSON. "
            "Please try generating again."
        )


# ============================================================
# CONTENT STRATEGY
# ============================================================

def generate_content_strategy(
    topic: str,
    audience: str,
    tone: str,
    platform: str,
) -> str:

    prompt = f"""
You are an expert YouTube content strategist.

Create a practical content strategy.

Topic: {topic}
Audience: {audience}
Tone: {tone}
Platform: {platform}

Return:

1. Content concept
2. Viewer problem or desire
3. Unique angle
4. Main promise
5. Suggested video structure
6. Viewer retention strategy
7. Call to action

Keep it practical and specific.
"""

    return ask_ai(prompt)


# ============================================================
# VIDEO IDEA
# ============================================================

def generate_video_idea(
    topic: str,
    audience: str,
    tone: str,
) -> str:

    prompt = f"""
Generate 5 strong YouTube video concepts.

Topic: {topic}
Audience: {audience}
Tone: {tone}

For each concept provide:
- Concept
- Why viewers would care
- Unique angle

Do not give generic ideas.
"""

    return ask_ai(prompt)


# ============================================================
# TITLES
# ============================================================

def generate_titles(
    topic: str,
    audience: str,
    tone: str,
) -> str:

    prompt = f"""
Generate 10 YouTube titles.

Topic: {topic}
Audience: {audience}
Tone: {tone}

Requirements:
- Clear
- Interesting
- Natural
- No fake claims
- Suitable for YouTube
- Mix curiosity, benefit and storytelling styles
"""

    return ask_ai(prompt)


# ============================================================
# HOOKS
# ============================================================

def generate_hooks(
    topic: str,
) -> str:

    prompt = f"""
Create 8 strong opening hooks for a YouTube video.

Topic:
{topic}

Each hook should be suitable for the first
5 to 15 seconds of a video.

Avoid generic introductions.
"""

    return ask_ai(prompt)


# ============================================================
# DESCRIPTION
# ============================================================

def generate_description(
    topic: str,
) -> str:

    prompt = f"""
Write a complete YouTube description.

Topic:
{topic}

Include:
- Strong opening
- What viewers will learn
- Natural keywords
- Call to action

Do not use keyword stuffing.
"""

    return ask_ai(prompt)


# ============================================================
# HASHTAGS
# ============================================================

def generate_hashtags(
    topic: str,
) -> str:

    prompt = f"""
Generate 15 relevant YouTube hashtags.

Topic:
{topic}

Return hashtags only.
"""

    return ask_ai(prompt)


# ============================================================
# KEYWORDS
# ============================================================

def generate_keywords(
    topic: str,
) -> str:

    prompt = f"""
Generate 20 useful YouTube SEO keywords.

Topic:
{topic}

Include:
- Main keywords
- Long-tail keywords
- Search-intent phrases
"""

    return ask_ai(prompt)


# ============================================================
# SCRIPT
# ============================================================

def generate_script(
    topic: str,
    audience: str,
    tone: str,
    video_length: str,
    language: str,
) -> str:

    prompt = f"""
Write a complete YouTube script.

Topic: {topic}
Audience: {audience}
Tone: {tone}
Length: {video_length}
Language: {language}

Structure:

HOOK
INTRODUCTION
MAIN CONTENT
EXAMPLES
TRANSITIONS
CONCLUSION
CALL TO ACTION

Make it natural for spoken delivery.

Do not describe the script as an essay.
Write it like something a creator would actually say.
"""

    return ask_ai(prompt)


# ============================================================
# STORYBOARD
# ============================================================

def generate_storyboard(
    topic: str,
    script: str,
    video_length: str,
) -> str:

    prompt = f"""
Create a detailed video storyboard.

Topic:
{topic}

Video length:
{video_length}

Script:
{script}

For every scene provide:

SCENE NUMBER
TIMESTAMP
DURATION
VISUAL
CAMERA SHOT
ACTION
VOICEOVER
ON-SCREEN TEXT
TRANSITION
VISUAL GENERATION PROMPT

Make the storyboard practical for actually producing
a video.
"""

    return ask_ai(prompt)


# ============================================================
# VISUAL ASSET PLAN
# ============================================================

def generate_visual_plan(
    topic: str,
    storyboard: str,
) -> str:

    prompt = f"""
Create a visual asset plan for this YouTube video.

Topic:
{topic}

Storyboard:
{storyboard}

Identify:
- Images required
- Video clips required
- B-roll
- Graphics
- Text overlays
- Background visuals
- Thumbnail requirements

For each asset provide a detailed generation/search prompt.
"""

    return ask_ai(prompt)


# ============================================================
# THUMBNAIL
# ============================================================

def generate_thumbnail_ideas(
    topic: str,
) -> str:

    prompt = f"""
Create 5 professional YouTube thumbnail concepts.

Topic:
{topic}

For each provide:
- Main visual
- Composition
- Short text
- Facial/emotional direction if appropriate
- Background
- Color/style direction
- Image-generation prompt
"""

    return ask_ai(prompt)


# ============================================================
# SCENE PLAN
# ============================================================

def generate_scene_plan(
    topic: str,
    video_length: str,
) -> str:

    prompt = f"""
Create a production-ready scene plan.

Topic:
{topic}

Length:
{video_length}

Include:
- Scene
- Approximate duration
- Visual
- Camera
- B-roll
- Voiceover purpose
- Text overlay
- Transition
"""

    return ask_ai(prompt)


# ============================================================
# YOUTUBE SHORT
# ============================================================

def generate_youtube_short(
    topic: str,
) -> str:

    prompt = f"""
Create a YouTube Short based on:

{topic}

Include:
- Hook
- 30-60 second script
- Visual directions
- On-screen text
- Ending CTA
"""

    return ask_ai(prompt)


# ============================================================
# INSTAGRAM REEL
# ============================================================

def generate_instagram_reel(
    topic: str,
) -> str:

    prompt = f"""
Create an Instagram Reel concept.

Topic:
{topic}

Include:
- First-second hook
- Short script
- Visual sequence
- On-screen text
- Caption
- CTA
"""

    return ask_ai(prompt)


# ============================================================
# REPURPOSED CONTENT
# ============================================================

def generate_repurposed_content(
    topic: str,
) -> str:

    prompt = f"""
Repurpose this YouTube topic into multiple platforms.

Topic:
{topic}

Create:

1. Instagram post
2. LinkedIn post
3. X/Twitter post
4. YouTube Community post
5. Short-form caption
6. Story idea

Keep each platform's style appropriate.
"""

    return ask_ai(prompt)


# ============================================================
# SEO
# ============================================================

def generate_seo_analysis(
    topic: str,
    titles: str,
    description: str,
    keywords: str,
) -> str:

    prompt = f"""
Analyze the YouTube SEO strategy.

Topic:
{topic}

Titles:
{titles}

Description:
{description}

Keywords:
{keywords}

Provide:

1. Search intent
2. Keyword relevance
3. Title suggestions
4. Description improvements
5. Keyword improvements
6. Thumbnail recommendations
7. Viewer-retention recommendations
"""

    return ask_ai(prompt)


# ============================================================
# COMPLETE CONTENT FACTORY
# ============================================================

def generate_content_factory(
    topic: str,
    audience: str,
    tone: str,
    video_length: str,
    language: str,
) -> dict[str, str]:

    idea = generate_video_idea(
        topic,
        audience,
        tone,
    )

    titles = generate_titles(
        topic,
        audience,
        tone,
    )

    hooks = generate_hooks(topic)

    description = generate_description(topic)

    hashtags = generate_hashtags(topic)

    keywords = generate_keywords(topic)

    script = generate_script(
        topic,
        audience,
        tone,
        video_length,
        language,
    )

    storyboard = generate_storyboard(
        topic,
        script,
        video_length,
    )

    visual_plan = generate_visual_plan(
        topic,
        storyboard,
    )

    thumbnail_ideas = generate_thumbnail_ideas(
        topic,
    )

    short = generate_youtube_short(topic)

    reel = generate_instagram_reel(topic)

    repurposed = generate_repurposed_content(
        topic,
    )

    seo = generate_seo_analysis(
        topic,
        titles,
        description,
        keywords,
    )

    return {
        "idea": idea,
        "titles": titles,
        "hooks": hooks,
        "description": description,
        "hashtags": hashtags,
        "keywords": keywords,
        "script": script,
        "storyboard": storyboard,
        "visual_plan": visual_plan,
        "thumbnail_ideas": thumbnail_ideas,
        "shorts": short,
        "reel": reel,
        "repurposed": repurposed,
        "seo": seo,
    }


# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================

def generate_youtube_idea(
    topic,
    audience,
    tone,
):
    return generate_video_idea(
        topic,
        audience,
        tone,
    )


def generate_youtube_titles(
    topic,
    audience,
    tone,
):
    return generate_titles(
        topic,
        audience,
        tone,
    )


def generate_youtube_description(topic):
    return generate_description(topic)


def generate_youtube_hashtags(topic):
    return generate_hashtags(topic)


def generate_youtube_keywords(topic):
    return generate_keywords(topic)


def generate_youtube_script(
    topic,
    audience,
    tone,
    video_length,
    language,
):
    return generate_script(
        topic,
        audience,
        tone,
        video_length,
        language,
    )


def generate_scene_by_scene_script(
    topic,
    video_length,
):
    return generate_scene_plan(
        topic,
        video_length,
    )


def generate_scene_by_scene(
    topic,
    video_length,
):
    return generate_scene_plan(
        topic,
        video_length,
    )


def generate_youtube_shorts(topic):
    return generate_youtube_short(topic)


def generate_shorts(topic):
    return generate_youtube_short(topic)


def generate_reel(topic):
    return generate_instagram_reel(topic)


def generate_seo(
    topic,
    titles,
    description,
    keywords,
):
    return generate_seo_analysis(
        topic,
        titles,
        description,
        keywords,
    )


def generate_thumbnail_image(
    prompt,
    output_path,
):
    """
    Placeholder for future image-generation integration.
    """
    raise NotImplementedError(
        "Image generation will be connected "
        "through the visual asset pipeline."
    )


# ============================================================
# SAVE TEXT CONTENT
# ============================================================

def save_youtube_content(
    content: str,
    filename: str = "outputs/youtube_content.txt",
):

    import os

    folder = os.path.dirname(filename)

    if folder:
        os.makedirs(
            folder,
            exist_ok=True,
        )

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(content)

    return filename