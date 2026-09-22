import os
import ollama

MODEL = "llama3.2"


def ask_ai(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


def generate_youtube_idea(topic, audience, tone, video_length, language):
    prompt = f"""
Generate 5 creative YouTube video ideas.

Topic: {topic}
Target audience: {audience}
Content style: {tone}
Video length: {video_length}
Language: {language}

Make each idea specific, interesting, suitable for the requested
audience and length, and write in the requested language.
Number the ideas 1 to 5.
"""
    return ask_ai(prompt)


def generate_youtube_titles(idea, audience, tone, video_length, language):
    prompt = f"""
Generate 5 catchy YouTube titles.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Video length: {video_length}
Language: {language}

Make them clear, interesting, clickable, suitable for YouTube,
not misleading, and appropriate for the audience.
Number them 1 to 5.
"""
    return ask_ai(prompt)


def generate_youtube_description(idea, audience, tone, video_length, language):
    prompt = f"""
Write an engaging YouTube description.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Video length: {video_length}
Language: {language}

Clearly explain the video, use relevant keywords naturally,
encourage viewers to watch, and write in the requested language.
"""
    return ask_ai(prompt)


def generate_youtube_hashtags(idea, audience, tone, video_length, language):
    prompt = f"""
Generate 10 relevant YouTube hashtags.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Video length: {video_length}
Language: {language}

Keep the hashtags relevant and suitable for YouTube.
"""
    return ask_ai(prompt)


def generate_youtube_keywords(idea, audience, tone, video_length, language):
    prompt = f"""
Generate 15 useful YouTube SEO keywords.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Video length: {video_length}
Language: {language}

Make them highly relevant to what the target audience may search.
Number them 1 to 15.
"""
    return ask_ai(prompt)


def generate_youtube_script(idea, audience, tone, video_length, language):
    prompt = f"""
Write a complete YouTube video script.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Video length: {video_length}
Language: {language}

Include:
- Strong introduction
- Main content
- Clear organization
- Natural conclusion

Follow the requested length and language.
"""
    return ask_ai(prompt)


def generate_thumbnail_ideas(idea, audience, tone, video_length, language):
    prompt = f"""
Generate 5 professional YouTube thumbnail ideas.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Video length: {video_length}
Language: {language}

For each idea include the main visual, subject, background,
composition, suggested text concept, and visual style.
Make each idea different and suitable for YouTube.
"""
    return ask_ai(prompt)


def generate_thumbnail_image(idea):
    from app.image_generator import (
        generate_thumbnail_image as generate_image
    )

    prompt = f"""
Create a professional YouTube thumbnail based on this idea:

{idea}

Photorealistic, professional photography, strong visual focus,
clear composition, cinematic lighting, detailed environment.
No text, letters, words, logos, or watermark.
"""
    return generate_image(prompt)


def generate_scene_by_scene_script(idea, audience, tone, video_length, language):
    prompt = f"""
Create a detailed scene-by-scene YouTube video plan.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Video length: {video_length}
Language: {language}

For every scene include:
- Scene number
- Approximate duration
- Visual/action
- Voice-over/dialogue
- On-screen text

Cover the requested video length and write in the requested language.
"""
    return ask_ai(prompt)


def generate_youtube_shorts(idea, audience, tone, language):
    prompt = f"""
Create a YouTube Shorts script.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Language: {language}

Start with a strong hook, keep it fast and engaging,
and finish with a natural call to action.
"""
    return ask_ai(prompt)


def generate_instagram_reel(idea, audience, tone, language):
    prompt = f"""
Create an Instagram Reel script.

Video idea: {idea}
Target audience: {audience}
Content style: {tone}
Language: {language}

Include an attention-grabbing hook, short engaging sections,
visual suggestions, and a natural call to action.
"""
    return ask_ai(prompt)


def generate_repurposed_content(idea, script, audience, tone, language):
    prompt = f"""
Repurpose this YouTube video into social media content.

Video idea: {idea}
Original script: {script}
Target audience: {audience}
Content style: {tone}
Language: {language}

Create:
1. YouTube Shorts version
2. Instagram Reel version
3. Instagram caption
4. LinkedIn post
5. Promotional post
"""
    return ask_ai(prompt)


def generate_seo_analysis(idea, titles, keywords, description):
    prompt = f"""
Analyze the SEO of this YouTube content.

Video idea: {idea}
Titles: {titles}
Keywords: {keywords}
Description: {description}

Provide:
1. Title SEO analysis
2. Keyword relevance
3. Description SEO analysis
4. Search intent
5. Missing keywords
6. Suggested improvements
7. SEO recommendations
"""
    return ask_ai(prompt)


def save_youtube_content(
    idea,
    titles,
    description,
    hashtags,
    keywords,
    script,
    thumbnail_ideas
):
    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/youtube_content.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("YOUTUBE CONTENT\n")
        file.write("============================\n\n")

        file.write("VIDEO IDEA\n")
        file.write("----------------------------\n")
        file.write(idea + "\n\n")

        file.write("TITLES\n")
        file.write("----------------------------\n")
        file