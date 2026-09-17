from agent import generate_youtube_idea, generate_youtube_titles


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