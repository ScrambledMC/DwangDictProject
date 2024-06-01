import xml.etree.ElementTree as et

tree = et.parse(r"c:\Users\The mom\Downloads\dwang.lift")
lift = tree.getroot()[-1]

def create_word(line):
    dwang, english, pos, notes = line.split("\t")

    entry = et.Element("entry")

    lexical_unit = et.SubElement(entry, "lexical-unit")
    lexical_unit.append(et.Element("form", lang="nnu-Latn"))
    dwang_et = et.SubElement(lexical_unit[0], "text")
    dwang_et.text = dwang

    entry.append(et.Element("trait", name="morph-type", value="stem"))

    if notes != "None":
        note = et.SubElement(entry, "note")
        note.append(et.Element("form", lang="en"))
        notes_et = et.SubElement(note[0], "text")
        notes_et.text = notes

    sense = et.SubElement(entry, "sense")
    if pos != "None":
        sense.append(et.Element("grammatical-info", value=pos))
    gloss = et.SubElement(sense, "gloss", lang="en")
    english_et = et.SubElement(gloss, "text")
    english_et.text = english

    return entry


with open(r"c:\Users\The mom\Downloads\new_wordlist.txt") as wordlist:
    for i in wordlist.readlines():
        lift.append(create_word(i))

tree.write(r"c:\Users\The mom\Downloads\dwang (1).lift")