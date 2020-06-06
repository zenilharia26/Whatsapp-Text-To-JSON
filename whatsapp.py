import re, json , sys

person1 = ""
person2 = ""
chat_file = ""
try :
    param1 = sys.argv[1]
    person1 = sys.argv[2]
    person2 = sys.argv[3]

    split_param = param1.split('.')
    if len(split_param) == 1 :
        chat_file = param1 + '.txt'

    elif split_param[-1] == 'txt' :
        chat_file = param1
    else :
        raise ValueError("")

except :
    print("pass cli arguments : 'file name'   'person1'  'person2'" )
    exit()

try :
    chat = open(chat_file, encoding='utf-8')
except : 
    print("no such file or directory")
    exit()

prev_time = ''
prev_sender = ''
lines = []
for line in chat:
    if re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{2}, [\d]{1,2}:[\d]{1,2} ", line):
        if (person1 in line) or (person2 in line):
            line_split = line.split()
            date = line_split[0][:-1]
            time = line_split[1] + " " + line_split[2]
            try:
                sender = line[line.index('-') + 2:line.index(':',line.index('-'))]
            except:
                print(line)
                continue
            msg = ' '.join(line_split[line_split.index(sender.split()[-1] + ':') + 1:])

            if prev_time == time and prev_sender == sender :
                try:
                    lines[-1][-1] += '\n ' + msg
                except:
                    print(line)
                    continue
            else :
                prev_sender = sender 
                prev_time = time
                lines.append([date,time,sender,msg]) #This means a whatsapp text.
    else:
        lines[-1][-1] += '\n ' + line[:-1] #For extra paragraphs or lines in messages.

data = {}
for [date,time,sender,message] in lines:

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

json_file_name =  chat_file[: -chat_file[::-1].index('.') - 1]+'.json' #Replace with name of the file you want.
with open(json_file_name, 'w') as chat:
    json.dump(data, chat, indent=3)

print("Completed ...")
     
