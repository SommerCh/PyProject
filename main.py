from buzzword import BUZZWORD, FORSLAG
from flask import Flask, render_template, request 


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
            print("Nyt buzzword:", new_word)

            if new_word != "":
                BUZZWORD.append(new_word)

        if "replace_word" in request.form:
            number = request.form["replace_word"]
            old_word = request.form["old_word_" + number]
            new_word = request.form["new_word_" + number]

            if new_word != "":
                text = replace_buzzword(text, old_word, new_word)

        found = find_buzzwords(text) 
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

# Find ord
def find_buzzwords(text): 
    """Søger og returnerer liste med buzzwords"""
    found = [] 

    for word in BUZZWORD: 
        if word.lower() in text.lower(): 

            found.append(word) 

    return found 

def replace_buzzword(text, old_word, new_word):
    """Erstatter buzzword med et nyt ord"""
    text = text.replace(old_word, new_word)
    return text

# Baggrunds farve
def color_words(text, found):
    """Baggrundsfarve til fundne buzzwords i mail"""
    color_text = text

    for word in found:
        color_text = color_text.replace(
            word,
            f"<span class='color'>{word}</span>"
        )

    return color_text

print("Virker")

app.run(port=5004)