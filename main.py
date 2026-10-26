from buzzword import BUZZWORD, FORSLAG
from flask import Flask, render_template, request 

class Buzzword:
    def __init__(self, wordlist):
        self.buzzwords = wordlist

    # Find ord
    def find_buzzwords(self, text):
        found = []

        for word in self.buzzwords:
            if word.lower() in text.lower():
                found.append(word)

        return found
    
    # Erstat ord
    def replace_buzzword(self, text, old_word, new_word):
        text = text.replace(old_word, new_word)
        return text

    # Tilføj ord
    def add_word(self, new):
        new_word = new.strip()
        if new_word == "": 
            return
            
        for word in self.buzzwords:
            if word.lower() == new_word.lower():
                return
                
        self.buzzwords.append(new_word)

    
buzzword_detector = Buzzword(BUZZWORD)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    # Initialisering    
    text=""
    found=[]
    word_count=0
    buzzword_number=0
    can_send_button=True
    color_text=""
    status_text=""
    status_color=""
    forslag=[]

    # Hent
    if request.method == "POST":
        text = request.form["mail"]

        # Tilføj
        if "add_word" in request.form:
            new_word = request.form["new_word"]
            buzzword_detector.add_word(new_word)
            print("Nyt buzzword:", new_word)

        if "replace_word" in request.form:
            number = request.form["replace_word"]
            old_word = request.form["old_word_" + number]
            new_word = request.form["new_word_" + number]

            if new_word != "":
                text = buzzword_detector.replace_buzzword(text, old_word, new_word)

        found = buzzword_detector.find_buzzwords(text) 
        word_count = len(text.split()) 
        buzzword_number = len(found) 

    # Antal buzzwords
    if buzzword_number <= 2:
        status_text = "Godkendt"
        status_color = "green"
        can_send_button = True
    elif buzzword_number <= 4:
        status_text = "Bør forbedres"
        status_color = "yellow"
        can_send_button = True
    else:
        status_text = "For mange buzzwords"
        status_color = "red"
        can_send_button = False

    return render_template(
        "index.html",
        text=text,
        found=found,
        word_count=word_count,
        buzzword_number=buzzword_number,
        can_send_button=can_send_button,
        color_text=color_text,
        status_text=status_text,
        status_color=status_color,
        forslag=forslag
    )


app.run(port=5004)
