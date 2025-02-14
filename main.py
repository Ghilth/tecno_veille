import streamlit as st
import pandas as pd
from article_search import search_articles

# -------------------------------
# 🎨 INTERFACE STREAMLIT 
# -------------------------------

# 🖼️ Configuration de la page
st.set_page_config(page_title="Veille Technologique", layout="wide", page_icon="🔍")

# 🌙 Mode sombre ou clair
st.markdown(
    """
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
        }
        .stTextInput>div>div>input {
            font-size: 18px !important;
            padding: 10px;
        }
        .result-box {
            padding: 15px;
            border-radius: 10px;
            background-color: white;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .result-title {
            font-size: 20px;
            font-weight: bold;
            color: #007BFF;
        }
        .result-excerpt {
            font-size: 14px;
            color: #333;
        }
        .result-meta {
            font-size: 12px;
            color: #666;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Interface principale
st.markdown("<h1 style='text-align: center;'>🔎 Veille Technologique</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Recherchez des articles scientifiques récents</p>", unsafe_allow_html=True)


# Saisie des mots-clés avec placeholder dynamique

search_query = st.text_input("Entrez vos mots-clés", placeholder="Ex: Intelligence Artificielle")


# Sélection de la plage d’années
col1, col2 = st.columns(2)
with col1:
    annee_debut = st.number_input("📅 Année de début", min_value=2000, max_value=2025, value=2018)
with col2:
    annee_fin = st.number_input("📅 Année de fin", min_value=2000, max_value=2025, value=2024)



# 🔍 Bouton de recherche
if st.button("🔍 Rechercher"):
    mots_cles = [mot.strip() for mot in search_query.split(",") if mot.strip()]
    
    if not mots_cles:
        st.warning("⚠️ Veuillez entrer au moins un mot-clé.")
    else:
        with st.spinner("🔄 Recherche en cours..."):
            resultats = search_articles(mots_cles, annee_debut, annee_fin)

        if resultats:
            st.success(f"✅ {len(resultats)} articles trouvés !")

            # 📄 Affichage des résultats
            for article in resultats:
                st.markdown(
                    f"""
                    <div class="result-box">
                        <a class="result-title" href="{article['Lien']}" target="_blank">{article['Titre']}</a>
                        <p class="result-excerpt">{article['Extrait']}</p>
                        <p class="result-meta">🖊️ {article['Auteur']} | 📅 {article['Année']} | 🔗 <a href="{article['Lien']}" target="_blank">Lire l'article</a></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # 📥 Téléchargement des résultats
            df = pd.DataFrame(resultats)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Télécharger les résultats (CSV)", csv, "articles.csv", "text/csv")
        else:
            st.warning("❌ Aucun article trouvé.")

st.markdown("---")
st.markdown("<p style='text-align: center;'>📚 Développé avec ❤️ en Python & Streamlit</p>", unsafe_allow_html=True)
