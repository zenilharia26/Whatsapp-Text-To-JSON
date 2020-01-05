import re, json

chat_file = 'chat.txt'

chat = open(chat_file, encoding='utf-8')
lines = []

flag = False
count = 0
for line in chat:
    if re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{2}", line):
        lines.append(line) #This means a whatsapp text.
    else:
        lines[-1] += line #For extra paragraphs or lines in messages.

data = {}

lines = [re.split(' ', line) for line in lines] #Splits the line considering spaces.

for line in lines:
    date = line[0][0:-1] #Date is present as "mm/dd/yy,"
    time = line[1]
    sender = line[3]+' '+line[4][0:-1] #Considering the name of the sender consists of first name and second name.
    message = ''
    for i in range(5,len(line)):
        message += line[i]+' ' #After the name, each data is a message.
    
    person1 = "First Person"
    person2 = "Second Person"
    #If the data is useful (i.e not change of number notification or encryption message) then store it in dictionary
    if (person1 in sender) or (person2 in sender):
        if date in data:
            if time in data[date]:
                data[date][time].append({"sender":sender, "message":message})
            else:
                data[date][time] = [{"sender":sender, "message":message}]
        else:
            data[date] = {}
            data[date][time] = [{"sender":sender, "message":message}]

json_file_name = 'chat.json' #Replace with name of the file you want.
with open(json_file_name, 'w') as chat:
    json.dump(data, chat, indent=3)
     
