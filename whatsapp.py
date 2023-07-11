import re
import sys
import json
import os

def convert_to_json(chat_file):
    try:
        chat_file = os.path.abspath(chat_file)
        if not chat_file.endswith(".txt"):
            raise ValueError("")
    except:
        print("Wrong file extension")
        return

    chat = open(chat_file, encoding='utf-8')
    message_regex = r'\[(\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}:\d{2} [APM]{2})\] ([^:]+): (.+)'
    lines = []

    for line in chat:
        line = line.strip()  # Remove leading/trailing whitespaces
        message_match = re.match(message_regex, line)
        if message_match:
            date_time = message_match.group(1)
            sender = message_match.group(2)
            text = message_match.group(3)
            lines.append([date_time, sender, text])
        elif lines:  # Add this condition to handle empty lines
            lines[-1][-1] += '\n' + line

    data = {}
    for [date_time, sender, text] in lines:
        date, time = date_time.split(', ')
        if date not in data:
            data[date] = {}
        if time not in data[date]:
            data[date][time] = []
        data[date][time].append({"sender": sender, "message": text})

    json_file_name = os.path.abspath(chat_file[:chat_file.index('.txt')] + '.json')
    with open(json_file_name, 'w') as json_file:
        json.dump(data, json_file, indent=3)

    print("Conversion successful. JSON file created:", json_file_name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the chat file name.")
    else:
        chat_file_name = sys.argv[1]
        convert_to_json(chat_file_name)
