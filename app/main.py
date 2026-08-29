from agent import generate_youtube_idea


print("🤖 Welcome to the YouTube Content Creation Agent!")

topic = input("\nEnter a topic for your YouTube channel: ")

print("\nGenerating YouTube video ideas...\n")

ideas = generate_youtube_idea(topic)

print("💡 Here are your YouTube video ideas:\n")
print(ideas)