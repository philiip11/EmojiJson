import json
import xml.etree.ElementTree as ElementTree

x = open("emoji4j.json").read()
j = json.loads(x)

root = ElementTree.parse("en.xml").getroot()

x = []
lastemoji = ""
e = {}
for annotation in root.findall('annotations/annotation'):
    emoji = annotation.get("cp")
    if lastemoji != emoji:
        lastemoji = emoji
        if e != {}:
            x.append(e)
        e = {"emoji": emoji}
    if annotation.get("type") == "tts":
        e["description"] = annotation.text
    else:
        e["tags"] = annotation.text
x.append(e)

f = open("emoji.json", "w")
f.write(json.dumps(x))
f.close()
