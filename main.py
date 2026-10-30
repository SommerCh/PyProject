from buzzword import BUZZWORDS
from flask import Flask, render_template, request 

class BuzzwordDetector:
    def __init__(self, wordlist):
        self.buzzwords = wordlist

    def find_buzzwords(self, text):
        found_buzzwords = []

        for word in self.buzzwords:
            if word.lower() in text.lower():
                found_buzzwords.append(word)
        return found_buzzwords
    
    def replace_buzzword(self, text, old_word, new_word):
        text = text.replace(old_word, new_word)
        return text

# Værdi for status 
OK_AMOUNT = 2
MAX_AMOUNT = 4

def get_status(buzzword_count):
    if buzzword_count <= OK_AMOUNT:
        return {"text": "Godkendt", "color": "green", "send": True}

    if buzzword_count <= MAX_AMOUNT:
        return {"text": "Bør forbedres", "color": "yellow", "send": True}
    return {"text": "For mange buzzwords", "color": "red", "send": False}

# Håndtere erstatning 
def handle_replace(text, form, buzzword_detector):
    if "replace_word" in form:
        word_index = form["replace_word"]
        old_word = form["old_word_" + word_index]
        new_word = form["new_word_" + word_index]
         
        if new_word != "":
            text = buzzword_detector.replace_buzzword(text, old_word, new_word)

    return text
    
buzzword_detector = BuzzwordDetector(BUZZWORDS)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    # Startværdier     
    text = ""
    found = []
    word_count = 0
    buzzword_count = 0

    if request.method == "POST":
        text = request.form["mail"]
        text = handle_replace(text, request.form, buzzword_detector)

        found = buzzword_detector.find_buzzwords(text) 
        word_count = len(text.split()) 
        buzzword_count = len(found)


    status = get_status(buzzword_count)
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
