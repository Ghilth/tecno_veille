import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
from article_search import search_articles, summarize

# Interface Streamlit
st.title("🔎 Academic Paper Search")
st.markdown("Recherchez des articles scientifiques et obtenez un résumé automatique.")

# Entrée utilisateur
keywords = st.text_input("🔍 Entrez un mot-clé ou une phrase :")
col1, col2 = st.columns(2)
start_year = col1.number_input("📅 Année de début", min_value=2000, max_value=2025, value=2022)
end_year = col2.number_input("📅 Année de fin", min_value=2000, max_value=2025, value=2025)
search_button = st.button("Rechercher")

# Vérification des entrées utilisateur
if search_button:
    if not keywords.strip():
        st.error("⚠️ Veuillez entrer un mot-clé valide.")
    elif start_year > end_year:
        st.error("⚠️ L'année de début ne peut pas être supérieure à l'année de fin.")
    else:
        with st.spinner("Recherche en cours..."):
            articles = search_articles(keywords, start_year, end_year)

        if not articles:  # Vérifie si `articles` est une liste valide
            st.warning("❌ Aucun article trouvé pour cette période.")
        else:
            st.success(f"✅ {len(articles)} articles trouvés")
            for article in articles:
                with st.expander(f"📌 {article.get('title', 'Titre inconnu')} ({article.get('year', 'Année inconnue')})"):
                    st.write(f"**📄 Extrait** : {article.get('snippet', 'Aucun extrait disponible')}")
                    st.write(f"**🔗 Lien** : [Lire l'article]({article.get('link', '#')})")
                    st.write(f"📊 **Citations** : {article.get('citations', 'Non disponible')}")
                    
                    # Ajout d'un bouton pour résumer l'article
                    if st.button(f"📖 Résumer : {article.get('title', 'Titre inconnu')}", key=article.get("link", "")):
                        with st.spinner("Génération du résumé..."):
                            summary = summarize(article.get("link", ""))
                        st.write("### ✍️ Résumé")
                        st.info(summary if summary else "Résumé non disponible.")
