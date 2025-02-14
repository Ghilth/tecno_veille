import streamlit as st
from article_search import search_articles

# Personnalisation de la page
st.set_page_config(page_title="Academic Paper Search", page_icon="🔎", layout="centered")

# Interface principale
st.markdown("<h1 style='text-align: center;'>🔎 Academic Paper Search</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Recherchez des articles scientifiques pertinents.</p>", unsafe_allow_html=True)

# Barre de recherche
with st.form("search_form"):
    st.markdown("### 🔍 Recherchez un article scientifique")
    keywords = st.text_input("**Entrez un mot-clé ou une phrase :**", placeholder="Exemple : intelligence artificielle")
    
    col1, col2 = st.columns(2)
    start_year = col1.number_input("📅 Année de début", min_value=2000, max_value=2025, value=2022)
    end_year = col2.number_input("📅 Année de fin", min_value=2000, max_value=2025, value=2025)

    # Bouton de recherche
    search_button = st.form_submit_button("🔎 Rechercher", use_container_width=True)

# Lancement de la recherche si le bouton est cliqué
if search_button:
    if not keywords.strip():
        st.error("⚠️ Veuillez entrer un mot-clé valide.")
    elif start_year > end_year:
        st.error("⚠️ L'année de début ne peut pas être supérieure à l'année de fin.")
    else:
        with st.spinner("🔄 Recherche en cours..."):
            articles = search_articles(keywords, start_year, end_year)

        # Affichage des résultats
        if not articles:
            st.warning("❌ Aucun article trouvé pour cette période.")
        else:
            st.success(f"✅ {len(articles)} articles trouvés")

            for article in articles:
                title = article.get('Titre', 'Titre inconnu')
                year = article.get('Année', 'Année inconnue')
                snippet = article.get('Extrait', 'Aucun extrait disponible')
                link = article.get('Lien', '')
                citations = article.get('Citations', 'Non disponible')

                with st.expander(f"📌 **{title}** ({year})"):
                    st.write(f"📝 **Extrait** : {snippet}")
                    
                    # Vérification si un lien est disponible
                    if link and link.startswith("http"):
                        st.markdown(f"🔗 [**Lire l'article**]({link})")
                    else:
                        st.write("🔗 Lien non disponible")

                    st.write(f"📊 **Citations** : {citations}")
