from agent import (
    generate_youtube_idea,
    generate_youtube_titles,
    generate_youtube_description,
    generate_youtube_hashtags,
    generate_youtube_script
) 
print("🤖 Welcome to the YouTube Content Creation Agent!")

topic = input("\nEnter a topic for your YouTube channel: ")

print("\nGenerating YouTube video ideas...\n")

ideas = generate_youtube_idea(topic)

print("💡 Here are your YouTube video ideas:\n")
print(ideas)

idea = input("\nEnter your chosen video idea: ")

print("\nGenerating YouTube titles...\n")

titles = generate_youtube_titles(idea)

print("🎬 Here are your YouTube title suggestions:\n")
print(titles)
print("\nGenerating YouTube description...\n")

description = generate_youtube_description(idea)

print("📝 YouTube description:\n")
print(description)
print("\nGenerating YouTube hashtags...\n")

hashtags = generate_youtube_hashtags(idea)

print("🏷️ YouTube hashtags:\n")
print(hashtags)
print("\nGenerating YouTube script...\n")

script = generate_youtube_script(idea)

print("🎥 YouTube video script:\n")
print(script)