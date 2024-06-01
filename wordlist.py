"""
Known issues:
Certain special characters (such as underlined characters) show up with weird symbols
Some words don't have multiple spaces between English and Dwang, which this algorithm relies on
-Currently those words are excluded

The word "Nuu" has the definition "dry up, el". Could the word "el" be a mistake?
"""

with open(r"c:\Users\The mom\Downloads\SIL COMPARATIVE AFRICAN WORDLIST.txt", encoding="UTF-8") as file:
    doc = file.readlines()


punctuation = ",.;:'\"<>`~/?!@#$%^&*()[]{}\\|-=_+"
unnecessary_punctuation = (".", "?", "!")
parts_of_speech = {
    "n": "Noun",
    "v": "Verb",
    "adv": "Adverb",
}

class Word:
    def __init__(self, english: str, dwang: str, notes: str=None, pos: str=None):
        self.english = english
        self.dwang = dwang
        self.notes = notes
        self.pos = pos

    def __str__(self):
        return f"{self.dwang}\t{self.english}\t{self.pos}\t{self.notes}"
#         return f"""Dwang word: {self.dwang}
# Meaning: {self.english}
# Part of speech: {self.pos}
# Notes: {self.notes}
# """


def raw_word(word: str) -> str:
    for i in punctuation:
        word = word.replace(i, "")
    return word

def remove_duplicates(l: list) -> list:
    for i, v in enumerate(l):
        if i and raw_word(l[i-1]) == raw_word(v):
            l.pop(i-1)
    return l


def create_word(line: str) -> Word:
    if "  " in line:
        english, dwang = line.split("  ", 1)
    else: return

    # Note: currently only leading and trailing commas are removed
    english = english.strip().strip(",").replace("ɔ", ")")
    for i in unnecessary_punctuation:
        english = english.replace(i, "")
    english = " ".join(remove_duplicates(english.split()[1:]))

    pos: str = None
    for i in parts_of_speech:
        try:
            ind: int = english.index("(" + i + ")")
        except: pass
        else:
            english = english[:ind] + english[ind + len(i) + 2:]
            pos = parts_of_speech[i]
            break

    dwang = dwang.strip()
    if not dwang: return
    if dwang.endswith(")") and "(" in dwang:
        dwang, notes = dwang.rsplit("(", 1)
        notes = notes[:-1]
    else: notes = None
    if dwang.startswith("ke̱/a"):
        dwang = "ke̱" + dwang[4:]

    return Word(english.strip(), dwang.strip(), notes, pos)
    

wordlist = []
for i in doc:
    word = create_word(i.strip().lower())
    if word: wordlist.append(word)


with open(r"c:\Users\The mom\Downloads\new_wordlist.txt", "w", encoding="UTF-8") as f:
    f.write("\n".join(map(str, wordlist)))