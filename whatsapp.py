import re, sys, json, os

try:
    chatFile = os.path.abspath(sys.argv[1])
    if not chatFile.endswith(".txt"):
        raise ValueError("")
except:
    print("Wrong file extension")

chat = open(chatFile, encoding='utf-8')
dateRegex = r"[\d]{1,2}/[\d]{1,2}/[\d]{2}"
timeRegex = r"[\d]{2}:[\d]{2}"
messageRegex = dateRegex+', '+timeRegex+' - *'
lines = []

for line in chat:
    messageIndex = re.search(messageRegex, line)
    if messageIndex != None and messageIndex.start() == 0:
        date = re.search(dateRegex, line).group(0)
        time = re.search(timeRegex, line).group(0)
        sender = line[line.index('-')+2 : line.index(':', line.index('-'))]
        text = line[line.index(':', line.index(sender))+2 : ]
        lines.append([date,time,sender,text])
    else:
        lines[-1][-1] += '\n' + line[:-1]

data = {}
for [date,time,sender,text] in lines:
    if not (date in data):
        data[date] = {}
    if not (time in data[date]):
        data[date][time] = []
    data[date][time].append({"sender":sender, "message":text})

jsonFileName = os.path.abspath(chatFile[:chatFile.index('.txt')]+'.json')
with open(jsonFileName, 'w') as jsonFile:
    json.dump(data, jsonFile, indent=3)
