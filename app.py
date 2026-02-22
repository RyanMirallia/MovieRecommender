import streamlit as st
import pickle
from recommender import NetflixRecommender

st.set_page_config(page_title="MovieRecommender", layout="centered")

@st.cache_resource
def get_engine():
    engine = NetflixRecommender()
    engine.load_data()
    
    import os
    matrix_path = 'data/similarity_matrix.pkl'
    
    if os.path.exists(matrix_path):
        with open(matrix_path, 'rb') as f:
            engine.cosine_sim = pickle.load(f)
    else:
        engine.build_recommender()
        
    return engine

recommender = get_engine()

st.title("🎬 Movie Recommender")
st.info("**Note:** This system uses the Netflix database updated until **2021**. Movies released after that date will not be included in the search results.")
with st.sidebar:
    st.title("About the Project")
    st.write("**Portfolio Project:** Developed to demonstrate skills in Data Science and NLP."
            " This website is non-commercial and has no affiliation with Netflix.")
    st.write("🛠️ **Technologies:** Python, Scikit-Learn, Streamlit, Sqlalchemy, Pandas")

escolha = st.selectbox(
    "Enter a movie title to receive five personalized recommendations. " \
    "Our algorithm analyzes metadata such as synopsis, cast, and director to ensure accurate suggestions.",
    options=recommender.df['title'].tolist(),
    index=None,
    placeholder="Ex: Matrix, Stranger Things..."
)

if escolha:
    st.subheader(f"Because You Watched {escolha}:")
    
    recomendacoes = recommender.get_recommendations(escolha)
    
    if isinstance(recomendacoes, list):
        for filme in recomendacoes:
            st.write(f"✅ {filme}")
    else:
        st.error(recomendacoes)