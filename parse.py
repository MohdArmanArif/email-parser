# Read Me
# Arguments:
# File Name: Any .pst (Required)
# Command: parse or browse (Default: parse)
# Assistants: Any number of "first_name last_name" (No assistants by default)

import pypff
import json
import re
import sys
from datetime import datetime as dt

def browse_folders(folder, depth=0, print_subj=False):
    indent = "    " * depth
    print(f"{indent}{folder.name} ({folder.number_of_sub_messages} messages)")

    # List messages in this folder
    if print_subj == True:
        for i in range(folder.number_of_sub_messages):
            try:
                message = folder.get_sub_message(i)
                print(f"{indent}  {message.subject}")
            except Exception as e:
                print(f"{indent}  Error reading message: {e}")

    # Recurse into subfolders
    for subfolder in folder.sub_folders:
        browse_folders(subfolder, depth + 1, print_subj)

def get_msg(folder):
    messages = {}

    # Get list of messages
    for i in range(folder.number_of_sub_messages):
        try:
            msg = folder.get_sub_message(i)
            if msg.subject != None:
                subject = msg.subject.replace("RE: ", "").replace("Re: ", "").replace("FW: ", "").strip()
            if subject not in messages:
                messages[subject] = [{
                    "Sender": msg.sender_name,
                    "Date": msg.delivery_time,
                    "Body": re.sub(r"<.*?>", "", msg.plain_text_body.decode("utf-8", errors="ignore").split("From: ")[0].replace("\r", "").replace("\n", ""))
                }]
            else:
                messages[subject].append({
                    "Sender": msg.sender_name,
                    "Date": msg.delivery_time,
                    "Body": re.sub(r"<.*?>", "", msg.plain_text_body.decode("utf-8", errors="ignore").split("From: ")[0].replace("\r", "").replace("\n", ""))
                })
        except Exception as e:
            print(f"Error reading message: {e}")

    # Recurse into subfolders
    for subfolder in folder.sub_folders:
        messages.update(get_msg(subfolder))

    return messages

def conv(messages, assistants=[]):

    convos = []
    for subject, conversation in messages.items():
        conversation.sort(key=lambda msg: msg["Date"])
        convo = []
        for i in range(len(conversation)):
            if conversation[i]["Sender"] in assistants: # "Arman Arif" "Tasin Disha" "Justin Jiang" "Kyle Hyatali" "Jacob Swiety"
                role = "Assistant"
            else:
                role = "User"
            convo.append({"Role": role, "Content": conversation[i]["Body"]})
        convos.append({"Subject": subject, "Conversation": convo})
    
    return convos

def parse(conversations):
    with open("pst2json_conversations.json", "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=2, ensure_ascii=False)

def open_pst(file_name):

    pst = pypff.file()
    pst.open(file_name)
    root = pst.get_root_folder()
    if len(sys.argv) > 2:
        if sys.argv[2] == "browse":
            browse_folders(root)
        elif sys.argv[2] == "parse":
            assistants = []
            if len(sys.argv) > 3:
                for i in range(3, len(sys.argv)):
                    assistants.append(sys.argv[i])
            parse(conv(get_msg(root), assistants))
        else:
            print("Incorrect Command (Type 'parse' or 'browse')")
    else:
        parse(conv(get_msg(root)))
    pst.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = sys.argv[1]
        open_pst(file)
    else:
        print("No file name provided.")