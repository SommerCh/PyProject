from buzzword import BUZZWORD
from flask import Flask, render_template, request 

class BuzzwordDetector:
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

# Status 
OK_AMOUNT = 2
MAX_AMOUNT = 4

def check_status(buzzword_number):
    if buzzword_number <= OK_AMOUNT:
        return {"text": "Godkendt", "color": "green", "send": True}

    if buzzword_number <= MAX_AMOUNT:
        return {"text": "Bør forbedres", "color": "yellow", "send": True}
    return {"text": "For mange buzzwords", "color": "red", "send": False}

# Erstat ord
def handle_replace(text, form):
    if "replace_word" in form:
        number = form["replace_word"]
        old_word = form["old_word_" + number]
        new_word = form["new_word_" + number]
         
        if new_word != "":
            text = buzzword_detector.replace_buzzword(text, old_word, new_word)

    return text
    
buzzword_detector = BuzzwordDetector(BUZZWORD)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    # Startværdier     
    text = ""
    found = []
    word_count = 0
    buzzword_number = 0

    if request.method == "POST":
        text = request.form["mail"]
        text = handle_replace(text, request.form)

        found = buzzword_detector.find_buzzwords(text) 
        word_count = len(text.split()) 
        buzzword_number = len(found)

    #Tjek/opdatere status
    status = check_status(buzzword_number)
    
    status_text = status["text"]
    status_color = status["color"]
    can_send_button = status["send"]   
     
# Til HTML
    return render_template(
        "index.html",
        text = text,
        found = found,
        word_count = word_count,
        can_send_button = can_send_button,
        status_text = status_text,
        status_color = status_color,
    )

app.run(port=5004)
