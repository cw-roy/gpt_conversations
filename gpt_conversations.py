import json
import os
import re

# Set directory path
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the JSON file
json_file_path = os.path.join(script_dir, 'conversations.json')
try:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        print("JSON file loaded successfully.")
except Exception as e:
    print(f"Error: {e}. Ensure the JSON file exists and is properly formatted.")
    exit(1)

# Function to sanitize filenames
def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '_', title)  # Replace invalid characters with '_'

# Function to extract questions and answers
def extract_conversations(conversation):
    conversations = []
    mapping = conversation.get('mapping', {})
    
    for node in mapping.values():
        message = node.get('message')
        if not isinstance(message, dict):  # Ensure message is a dictionary
            continue
        
        author_role = message.get('author', {}).get('role')
        parts = message.get('content', {}).get('parts', [])
        
        if parts:
            if author_role == 'user':
                conversations.append(f"Q: {parts[0]}")
            elif author_role == 'assistant':
                conversations.append(f"A: {parts[0]}")
    
    return conversations

# Function to write conversations to a text file
def write_conversation_to_file(title, conversations):
    if not conversations:
        print(f"Skipping '{title}' as it has no valid messages.")
        return
    
    filename = f"{sanitize_filename(title)}.txt"
    filepath = os.path.join(script_dir, filename)
    try:
        with open(filepath, 'w') as file:
            for conversation in conversations:
                file.write(conversation + '\n')
        print(f"Conversations written to file: {filename}")
    except Exception as e:
        print(f"Failed to write to file: {e}")

# List conversation titles
titles = [conversation.get('title', 'Untitled') for conversation in data]
print("Available conversations:")
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")
print(f"{len(titles) + 1}. Export all conversations")

# Get user selection with validation
while True:
    selection = input("Select a conversation to export (enter the number): ")
    if selection.isdigit():
        selection = int(selection)
        if 1 <= selection <= len(titles) + 1:
            break
    print("Invalid input. Please enter a valid number.")

# Export selected conversation(s)
if selection == len(titles) + 1:
    # Export all conversations
    for conversation in data:
        title = conversation.get('title', 'Untitled')
        conversations = extract_conversations(conversation)
        write_conversation_to_file(title, conversations)
elif 1 <= selection <= len(titles):
    # Export selected conversation
    conversation = data[selection - 1]
    title = conversation.get('title', 'Untitled')
    conversations = extract_conversations(conversation)
    write_conversation_to_file(title, conversations)
else:
    print("Invalid selection.")


# import json
# import os

# # Set directory path
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Load the JSON file
# json_file_path = os.path.join(script_dir, 'conversations.json')
# try:
#     with open(json_file_path, 'r') as file:
#         data = json.load(file)
#         print("JSON file loaded successfully.")
# except Exception as e:
#     print(f"Failed to load JSON file: {e}")
#     exit(1)

# # Function to extract questions and answers
# def extract_conversations(conversation):
#     conversations = []
#     mapping = conversation.get('mapping', {})
#     for node_id, node in mapping.items():
#         message = node.get('message')
#         if message:
#             if message['author']['role'] == 'user' and 'parts' in message['content']:
#                 question = message['content']['parts'][0]
#                 conversations.append(f"Q: {question}")
#             elif message['author']['role'] == 'assistant' and 'parts' in message['content']:
#                 answer = message['content']['parts'][0]
#                 conversations.append(f"A: {answer}")
#     return conversations

# # Function to write conversations to a text file
# def write_conversation_to_file(title, conversations):
#     filename = f"{title}.txt"
#     filepath = os.path.join(script_dir, filename)
#     try:
#         with open(filepath, 'w') as file:
#             for conversation in conversations:
#                 file.write(conversation + '\n')
#         print(f"Conversations written to file: {filename}")
#     except Exception as e:
#         print(f"Failed to write to file: {e}")

# # List conversation titles
# titles = [conversation['title'] for conversation in data]
# print("Available conversations:")
# for i, title in enumerate(titles, 1):
#     print(f"{i}. {title}")
# print(f"{len(titles) + 1}. Export all conversations")

# # Get user selection
# selection = input("Select a conversation to export (enter the number): ")

# # Export selected conversation(s)
# if selection.isdigit():
#     selection = int(selection)
#     if selection == len(titles) + 1:
#         # Export all conversations
#         for conversation in data:
#             title = conversation['title']
#             conversations = extract_conversations(conversation)
#             write_conversation_to_file(title, conversations)
#     elif 1 <= selection <= len(titles):
#         # Export selected conversation
#         conversation = data[selection - 1]
#         title = conversation['title']
#         conversations = extract_conversations(conversation)
#         write_conversation_to_file(title, conversations)
#     else:
#         print("Invalid selection.")
# else:
#     print("Invalid input.")
