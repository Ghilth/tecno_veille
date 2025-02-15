import http.client
import json
import requests
from dotenv import load_dotenv
import os




load_dotenv()  # Charge les variables depuis .env
api_key = os.getenv("api_key")  # Récupère la clé API


def search_articles(mots_cles, annee_debut=None, annee_fin=None):
    if not api_key:
        raise ValueError("La clé API est manquante !")

    print("🔑 Clé API utilisée :", api_key)  # Debugging

    # Connexion à l'API
    conn = http.client.HTTPSConnection("google.serper.dev")
    
    # Préparer le payload correctement
    payload = json.dumps({"q": " ".join(mots_cles)})
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    # Envoyer la requête POST
    conn.request("POST", "/scholar", payload, headers)
    res = conn.getresponse()
    
    # Vérification du statut de la réponse
    if res.status != 200:
        print(f"❌ Erreur API ({res.status}):", res.read().decode("utf-8"))
        return []

    data = res.read()
    print("📜 Réponse brute de l'API:", data[:500])  # Afficher seulement une partie pour éviter trop d'affichage
    
    try:
        articles = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        print("❌ Erreur de décodage JSON")
        return []

    # Liste des résultats
    resultats = []
    
    # Parcourir les résultats
    for article in articles.get("organic", []):
        annee_article = article.get("year", None)
        
        # Appliquer le filtre de date
        if annee_debut and annee_article and int(annee_article) < annee_debut:
            continue
        if annee_fin and annee_article and int(annee_article) > annee_fin:
            continue
        
        # Extraire les informations utiles
        info_article = {
            "Titre": article.get("title", ""),
            "Lien": article.get("link", ""),
            "Extrait": article.get("snippet", ""),
            "Auteur": article.get("author", ""),
            "Année": annee_article,
            "Citations": article.get("citedBy", ""),
        }
        resultats.append(info_article)
    
    return resultats

# Exemple d'utilisation
mots_cles = ["model deployment", "deep learning"]
annee_debut = 2018
annee_fin = 2024

resultats = search_articles(mots_cles, annee_debut, annee_fin)
print(resultats)