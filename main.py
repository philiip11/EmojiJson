import json
import xml.etree.ElementTree as ElementTree

# Parse XML
x = []
lastemoji = ""
e = {}
root = ElementTree.parse("en.xml").getroot()
for annotation in root.findall('annotations/annotation'):
    emoji = annotation.get("cp")
    if lastemoji != emoji:
        lastemoji = emoji
        if e != {}:
            x.append(e)
        e = {"emoji": emoji}
    if annotation.get("type") == "tts":
        e["description"] = annotation.text.split()
    else:
        tags = annotation.text.split("|")
        e["tags"] = [i.strip() for i in tags]
x.append(e)

# Parse JSON
y = open("emoji4j.json", encoding="utf8").read()
j = json.loads(y)
for e in j:
    for o in x:
        if o["emoji"] == e["emoji"]:
            o["aliases"] = e["aliases"]
            if "emoticons" in e:
                o["emoticons"] = e["emoticons"]

# Parse TXT
fileHandler = open("groups.txt", "r", encoding="utf8")
listOfLines = fileHandler.readlines()
fileHandler.close()
for line in listOfLines:
    if line[0:8] == "# group:":
        group = line[9:].strip()
        print(group)
    if line[0:11] == "# subgroup:":
        subgroup = line[12:].strip()
        print("--" + subgroup)
    if len(line) > 70:
        if line[65] == "#":
            emoji = line[67:69].strip()
            print(emoji)
            for o in x:
                if o["emoji"] == emoji:
                    o["group"] = group
                    o["subgroup"] = subgroup

f = open("emoji.json", "w", encoding="utf8")
f.write(json.dumps(x))
f.close()
