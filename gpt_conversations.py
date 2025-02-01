import json
import os

# Load the JSON file
try:
    with open('/home/riggs/code/gpt_conversations/conversations.json', 'r') as file:
        data = json.load(file)
        print("JSON file loaded successfully.")
except Exception as e:
    print(f"Failed to load JSON file: {e}")
    exit(1)

# Function to extract questions and answers
def extract_conversations(conversation):
    conversations = []
    mapping = conversation.get('mapping', {})
    for node_id, node in mapping.items():
        message = node.get('message')
        if message:
            if message['author']['role'] == 'user' and 'parts' in message['content']:
                question = message['content']['parts'][0]
                conversations.append(f"Q: {question}")
            elif message['author']['role'] == 'assistant' and 'parts' in message['content']:
                answer = message['content']['parts'][0]
                conversations.append(f"A: {answer}")
    return conversations

# Function to write conversations to a text file
def write_conversation_to_file(title, conversations):
    filename = f"{title}.txt"
    filepath = os.path.join('/home/riggs/code/gpt_conversations', filename)
    try:
        with open(filepath, 'w') as file:
            for conversation in conversations:
                file.write(conversation + '\n')
        print(f"Conversations written to file: {filename}")
    except Exception as e:
        print(f"Failed to write to file: {e}")

# List conversation titles
titles = [conversation['title'] for conversation in data]
print("Available conversations:")
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")
print(f"{len(titles) + 1}. Export all conversations")

# Get user selection
selection = input("Select a conversation to export (enter the number): ")

# Export selected conversation(s)
if selection.isdigit():
    selection = int(selection)
    if selection == len(titles) + 1:
        # Export all conversations
        for conversation in data:
            title = conversation['title']
            conversations = extract_conversations(conversation)
            write_conversation_to_file(title, conversations)
    elif 1 <= selection <= len(titles):
        # Export selected conversation
        conversation = data[selection - 1]
        title = conversation['title']
        conversations = extract_conversations(conversation)
        write_conversation_to_file(title, conversations)
    else:
        print("Invalid selection.")
else:
    print("Invalid input.")
