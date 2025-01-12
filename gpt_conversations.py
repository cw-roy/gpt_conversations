import json

# Load the JSON file
try:
    with open('/home/riggs/code/gpt_conversations/conversations.json', 'r') as file:
        data = json.load(file)
        print("JSON file loaded successfully.")
except Exception as e:
    print(f"Failed to load JSON file: {e}")
    exit(1)

# Function to extract questions and answers
def extract_conversations(data):
    conversations = []
    for conversation in data:
        print(f"Inspecting conversation: {conversation.get('title', 'No Title')}")  # Debug print
        mapping = conversation.get('mapping', {})
        for node_id, node in mapping.items():
            print(f"Inspecting node: {node_id}")  # Debug print
            message = node.get('message')
            if message:
                print(f"Found message: {message}")  # Debug print
                if message['author']['role'] == 'user' and 'parts' in message['content']:
                    question = message['content']['parts'][0]
                    conversations.append(f"Q: {question}")
                    print(f"Extracted question: {question}")  # Debug print
                elif message['author']['role'] == 'assistant' and 'parts' in message['content']:
                    answer = message['content']['parts'][0]
                    conversations.append(f"A: {answer}")
                    print(f"Extracted answer: {answer}")  # Debug print
    print(f"Total conversations extracted: {len(conversations)}")  # Debug print
    return conversations

# Extract conversations
conversations = extract_conversations(data)

# Write to a text file
try:
    with open('/home/riggs/code/gpt_conversations/conversations.txt', 'w') as file:
        for conversation in conversations:
            file.write(conversation + '\n')
            print(f"Written to file: {conversation}")  # Debug print
    print("Conversations written to file successfully.")
except Exception as e:
    print(f"Failed to write to file: {e}")

print("Conversations extracted successfully.")