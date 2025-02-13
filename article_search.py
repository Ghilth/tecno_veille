import http.client
import json
import requests
from bs4 import BeautifulSoup
import os
from transformers import pipeline



#load key
api_key = os.getenv("api_key")



def summarize(lien):
    # Étape 1: Récupérer le contenu de la page
    try:
        response = requests.get(lien)
        response.raise_for_status()  # Vérifie si la requête a réussi
        page_content = response.text
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la récupération de la page : {e}"
    

    # Étape 2: Extraire le texte de l'article
    soup = BeautifulSoup(page_content, "html.parser")

    
    # En fonction de la structure du site, tu devras peut-être ajuster ceci
    paragraphs = soup.find_all('p')  # Extraire tous les paragraphes <p>
    
    # Joindre les paragraphes pour former le texte complet de l'article
    article_text = " ".join([para.get_text() for para in paragraphs])
    
    # Étape 3: Utiliser un modèle pour générer le résumé
    summarizer = pipeline("summarization")  # Pipeline de résumé de Hugging Face
    
    # Diviser le texte en morceaux si nécessaire (limite de longueur pour le modèle)
    max_input_length = 2000  # La limite de tokens pour de nombreux modèles GPT-2 et GPT-3
    
    if len(article_text) > max_input_length:
        article_text = article_text[:max_input_length]  # Prendre une portion du texte

    # Résumer l'article
    summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)
    
    return summary[0]['summary_text']




def search_articles(mots_cles, annee_debut=None, annee_fin=None):
    # Connexion à l'API
    conn = http.client.HTTPSConnection("google.serper.dev")
    
    # Préparer le payload (les mots-clés sous forme de requêtes)
    payload = json.dumps([{"q": mot} for mot in mots_cles])
    
    headers = {
        'X-API-KEY': api_key,  # Remplace avec ta propre clé API
        'Content-Type': 'application/json'
    }
    
    # Envoyer la requête POST
    conn.request("POST", "/scholar", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    # Convertir la réponse en format JSON
    articles = json.loads(data.decode("utf-8"))
    
    # Liste pour stocker les résultats
    resultats = []
    
    # Parcourir les résultats de chaque requête (mots-clés)
    for resultat in articles:
        for article in resultat.get("organic", []):
            # Récupérer l'année de l'article
            annee_article = article.get("year", None)
            
            # Si une plage d'années est définie, on filtre les articles
            if annee_debut and annee_article and int(annee_article) < annee_debut:
                continue
            if annee_fin and annee_article and int(annee_article) > annee_fin:
                continue
            
            # Extraire les informations pertinentes
            info_article = {
                "Titre": article.get("title", ""),
                "Lien": article.get("link", ""),
                "Extrait": article.get("snippet", ""),
                "Resume": summarize(article.get("link", "")),
                "Auteur": article.get("author", ""),
                "Année": annee_article,
                "Citations": article.get("citedBy", "")
            }
            resultats.append(info_article)
    
    return resultats


# Exemple d'utilisation avec tranche d'années
mots_cles = ["model depoyment", "deep learning"]
annee_debut = 2018
annee_fin = 2024

search_articles(mots_cles,annee_debut,annee_fin)