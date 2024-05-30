import base64
import json
import random
from flask import Flask, render_template, request, session
from flask_session import Session
from bs4 import BeautifulSoup
import requests
import re
import os
from requests import post,get

dico = {
    'Afghanistan': 'Asie',
    'Albanie': 'Europe',
    'Algérie': 'Afrique',
    'Argentine': 'Amérique du Sud',
    'Australie': 'Océanie',
    'Autriche': 'Europe',
    'Bangladesh': 'Asie',
    'Belgique': 'Europe',
    'Brésil': 'Amérique du Sud',
    'Canada': 'Amérique du Nord',
    'Chine': 'Asie',
    'Colombie': 'Amérique du Sud',
    'République tchèque': 'Europe',
    'Danemark': 'Europe',
    'Égypte': 'Afrique',
    'Éthiopie': 'Afrique',
    'Finlande': 'Europe',
    'France': 'Europe',
    'Allemagne': 'Europe',
    'Grèce': 'Europe',
    'Hongrie': 'Europe',
    'Inde': 'Asie',
    'Indonésie': 'Asie',
    'Iran': 'Asie',
    'Irak': 'Asie',
    'Irlande': 'Europe',
    'Israël': 'Asie',
    'Italie': 'Europe',
    'Japon': 'Asie',
    'Jordanie': 'Asie',
    'Kenya': 'Afrique',
    'Liban': 'Asie',
    'Libye': 'Afrique',
    'Malaisie': 'Asie',
    'Mexique': 'Amérique du Nord',
    'Maroc': 'Afrique',
    'Népal': 'Asie',
    'Pays-Bas': 'Europe',
    'Nouvelle-Zélande': 'Océanie',
    'Nigéria': 'Afrique',
    'Norvège': 'Europe',
    'Pakistan': 'Asie',
    'Pérou': 'Amérique du Sud',
    'Philippines': 'Asie',
    'Pologne': 'Europe',
    'Portugal': 'Europe',
    'Roumanie': 'Europe',
    'Russie': 'Europe',
    'Arabie saoudite': 'Asie',
    'Singapour': 'Asie',
    'Afrique du Sud': 'Afrique',
    'Corée du Sud': 'Asie',
    'Espagne': 'Europe',
    'Sri Lanka': 'Asie',
    'Soudan': 'Afrique',
    'Suède': 'Europe',
    'Suisse': 'Europe',
    'Syrie': 'Asie',
    'Thaïlande': 'Asie',
    'Tunisie': 'Afrique',
    'Turquie': 'Europe',
    'Ouganda': 'Afrique',
    'Ukraine': 'Europe',
    'Émirats arabes unis': 'Asie',
    'Royaume-Uni': 'Europe',
    'États-Unis': 'Amérique du Nord',
    'Venezuela': 'Amérique du Sud',
    'Viêt Nam': 'Asie',
    'Yémen': 'Asie',
    'Zimbabwe': 'Afrique',
    'Islande': 'Europe',
    'Luxembourg': 'Europe',
    'Monaco': 'Europe',
    'Saint-Marin': 'Europe',
    'Liechtenstein': 'Europe',
    'Malte': 'Europe',
    'Andorre': 'Europe',
    'Lettonie': 'Europe',
    'Estonie': 'Europe',
    'Lituanie': 'Europe',
    'Slovaquie': 'Europe',
    'Slovénie': 'Europe',
    'Croatie': 'Europe',
    'Bosnie-Herzégovine': 'Europe',
    'Serbie': 'Europe',
    'Monténégro': 'Europe',
    'Macédoine du Nord': 'Europe',
    'Kosovo': 'Europe',
    'Arménie': 'Asie',
    'Azerbaïdjan': 'Asie',
    'Géorgie': 'Europe',
    'Kazakhstan': 'Asie',
    'Koweït': 'Asie',
    'Oman': 'Asie',
    'Qatar': 'Asie',
    'Bahreïn': 'Asie',
    'Chypre': 'Europe',
    'Bhoutan': 'Asie',
    'Maldives': 'Asie',
    'Bolivie': 'Amérique du Sud',
    'Paraguay': 'Amérique du Sud',
    'Uruguay': 'Amérique du Sud',
    'Guyana': 'Amérique du Sud',
    'Suriname': 'Amérique du Sud',
    'Equateur': 'Amérique du Sud',
    'Chili': 'Amérique du Sud',
    'Honduras': 'Amérique centrale',
    'Guatemala': 'Amérique centrale',
    'Salvador': 'Amérique centrale',
    'Nicaragua': 'Amérique centrale',
    'Costa Rica': 'Amérique centrale',
    'Panama': 'Amérique centrale',
    'Jamaïque': 'Caraïbes',
    'Bahamas': 'Caraïbes',
    'Barbade': 'Caraïbes',
    'Cuba': 'Caraïbes',
    'Haïti': 'Caraïbes',
    'Madagascar': 'Afrique',
    'Turkménistan': 'Asie',
    'Ouzbékistan': 'Asie',
    'Kirghizistan': 'Asie',
}


app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def chooseNewCountry():
    Limgs = []
    session["country"], session["continent"] = random.choice(list(dico.items()))
    url = "https://www.bing.com/images/search?q="+session["country"]+"+city&form=HDRSC4&first=1"
    html_data = requests.get(url).text
    soup = BeautifulSoup(html_data, "html.parser")
    divTag = soup.find_all("div",id="b_content")
    soup2 = BeautifulSoup(str(divTag), "html.parser")
    imgTags = soup2.find_all("a")
    pattern = r'murl":"(.*?)",'
    for i in imgTags:
        match = re.search(pattern, str(i))
        if match:
            extracted_text = match.group(1)
            Limgs.append(extracted_text)

    session["img"] = random.choice(Limgs)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        session["continentFoud"] = 0
        session["country"]= ""
        session["continent"] = ""
        session["img"] = ""
        textVar = "D'où vient ce paysage ??"
        session["textContinent"] = "?"
        chooseNewCountry()
    elif request.method == 'POST':
        if session["continentFoud"] == 0:
            name = request.form["name"]
            if name in dico :
                if dico[name] == session["continent"]:
                    session["continentFound"] = 1
                    session["textContinent"] = session["continent"]
                if name == session["country"]:
                    textVar = "Bravo c'était bien "+name
                else :
                    textVar = "Non essaye encore..." 
            else :
                textVar = "Pays Inconnu" 
    return render_template("index.html",continent=session["textContinent"],img = session["img"],textVar = textVar,data = dico)

@app.route('/showansw', methods=['GET', 'POST'])
def answr():
    textVar = "C'était "+session["country"]
    return render_template("index.html",continent=session["continent"],img = session["img"],textVar = textVar,data = dico)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))