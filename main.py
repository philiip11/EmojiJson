import json
import xml.etree.ElementTree as ElementTree
import urllib.request

annotationsURL = "https://raw.githubusercontent.com/unicode-org/cldr/master/common/annotations/en.xml"
emoji4jURL = "https://raw.githubusercontent.com/kcthota/emoji4j/master/src/main/resources/emoji.json"
groupsURL = "https://unicode.org/Public/emoji/12.0/emoji-test.txt"

urllib.request.urlretrieve(annotationsURL, "en.xml")
print("DONE en.xml")
urllib.request.urlretrieve(emoji4jURL, "emoji4j.json")
print("DONE emoji4j.json")
urllib.request.urlretrieve(groupsURL, "groups.txt")
print("DONE groups.txt")
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
        e["description"] = [annotation.text]
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
group = "NONE"
subgroup = "NONE"
for line in listOfLines:
    if line[0:8] == "# group:":
        group = line[9:].strip()
        print(group)
    if line[0:11] == "# subgroup:":
        subgroup = line[12:].strip()
        print("--" + subgroup)
    if len(line) > 70 and line[65] == "#":
        emoji = line[67:69].strip()
        print(emoji)
        for o in x:
            if o["emoji"] == emoji:
                o["group"] = group
                o["subgroup"] = subgroup

#Add Aliases for chat-tools like :smile: or :kangaroo:
for emoji in x:
    if "aliases" not in emoji.keys():
        emoji["aliases"] = [emoji["description"][0].replace(" ", "_")]

f = open("emoji.json", "w", encoding="utf8")
f.write(json.dumps(x))
f.close()
