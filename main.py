from buzzword import BUZZWORD, FORSLAG
from flask import Flask, render_template, request 

# Bruger 3 ting fra flask; 
# Flask til at gøre det til en webudgave.
# Render template til at vise HTML-side og sende data fra Python videre til din HTML (aom antal ord)
# Request til at hente det brugeren sender fra browseren.

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])

def home():

# Typer    
    text = ""
    found = []
    wordCount = 0
    buzzWordNumber = 0
    canSendButton = True
    colorText = ""
    statusText = ""
    statusColor = ""
    forslag = []
  

# Hent
    if request.method == "POST":
        text = request.form["mail"]

        # if "deleteWord" in request.form:  # Den er nødt til at være før found = findBuzzwords(text)
        #     word = request.form["deleteWord"]
            
        #     BUZZWORD.remove(word)

        if "addWord" in request.form:
            newWord = request.form["newWord"]
            print("Nyt buzzword:", newWord)

            if newWord != "":
                BUZZWORD.append(newWord)

        if "replaceWord" in request.form:
            number = request.form["replaceWord"]
            oldWord = request.form["oldWord_" + number]
            newWord = request.form["newWord_" + number]

            if newWord != "":
                text = erstatBuzzword(text, oldWord, newWord)

        found = findBuzzwords(text) # Sender teksten ind i funktionen findBuzzwords(). Ordene gemmes i found.
        wordCount = len(text.split()) # Opdeler teksten i ord. len() tæller ordene. Tallet gemmes i wordCount
        buzzWordNumber = len(found) # Listen med fundne buzzwords. len() tæller, hvor mange forskellige buzzwords listen indeholder. Tallet gemmes i buzzWordNumber


# Antal buzzwords
    if buzzWordNumber <= 2:
        statusText = "Godkendt"
        statusColor = "green"
        canSendButton = True
    elif buzzWordNumber <= 4:
        statusText = "Bør forbedres"
        statusColor = "yellow"
        canSendButton = True
    else:
        statusText = "For mange buzzwords"
        statusColor = "red"
        canSendButton = False


# Python og HTML deler ikke data. Åbner og viser index.html. Sender Python-variablerne til HTML.
# Venstre side = Navnet i HTML - Højre side = Navnet i Python
    return render_template(
        "index.html",
        text = text,
        found = found,
        wordCount = wordCount,
        buzzWordNumber = buzzWordNumber,
        canSendButton = canSendButton,
        colorText = colorText,
        statusText = statusText,
        statusColor = statusColor,
        forslag = forslag
    )


# Find ord
def findBuzzwords(text): # Opretter funktionen findBuzzwords. Den modtager en tekst.
    found = [] # Opretter en tom liste, hvor de fundne buzzwords skal gemmes.

    for word in BUZZWORD: # Gennemgår hvert ord i listen BUZZWORD, ét ad gangen.
        if word.lower() in text.lower(): # Undersøger, om ordet findes i teksten. Gør det til små bogstaver

            found.append(word) # Hvis ordet findes, tilføjes det til listen found.

    return found # Sender listen med de fundne buzzwords tilbage til stedet, hvor funktionen blev kaldt:


# Find forslag
# def findForslag(found):
#     forslag = []

#     for word in found:
#         if word in FORSLAG:
#             forslag.append({
#                 "word": word,
#                 "forslag": FORSLAG[word]
#             })

#     return forslag


def erstatBuzzword(text, oldWord, newWord):
    text = text.replace(oldWord, newWord)
    return text


# Baggrunds farve
def colorWords(text, found):
    colorText = text

    for word in found:
        colorText = colorText.replace(
            word,
            f"<span class='color'>{word}</span>"
        )

    return colorText



# test_text = "Vi skal skabe alignment og arbejde mere agilt fremadrettet"
# print(findBuzzwords(test_text))


print("Virker")

app.run(port=5004)