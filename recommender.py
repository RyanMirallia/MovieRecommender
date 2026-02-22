import pandas as pd
import sqlite3
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class NetflixRecommender:
    def __init__(self, db_path='data/netflix.db'):
        self.db_path = db_path
        self.df = None
        self.cosine_sim = None
        self.indices = None

    def load_data(self):
        
        conn = sqlite3.connect(self.db_path)
        
        self.df = pd.read_sql_query("SELECT * FROM titles", conn)
        conn.close()
        
        cols_to_fix = ['director', 'cast', 'country', 'description', 'listed_in']
        self.df[cols_to_fix] = self.df[cols_to_fix].fillna('')
        
        self.df['soup'] = (
            self.df['description'] + ' ' + 
            self.df['listed_in'] + ' ' + 
            self.df['cast'] + ' ' + 
            self.df['director']
        ).str.lower()
        
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()

    def build_recommender(self):

        print("Iniciando a construção da matriz de similaridade...")
        
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.df['soup'])
        
        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        
        with open('data/similarity_matrix.pkl', 'wb') as f:
            pickle.dump(self.cosine_sim, f)
            
        print("Mecanismo construído e salvo em: data/similarity_matrix.pkl")

    def get_recommendations(self, title, top_n=5):
       
        if title not in self.indices:
            return f"Erro: O título '{title}' não foi encontrado no banco de dados."
            
        idx = self.indices[title]
        
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        movie_indices = [i[0] for i in sim_scores[1:top_n+1]]
        
        return self.df['title'].iloc[movie_indices].tolist()


if __name__ == "__main__":
    recommender = NetflixRecommender()
    
    print("1. Carregando dados...")
    recommender.load_data()
    
    print("2. Construindo motor de busca...")
    recommender.build_recommender()
    
    #Teste
    filme_teste = 'Stranger Things'
    print(f"\n--- Recomendações para: {filme_teste} ---")
    resultados = recommender.get_recommendations(filme_teste)
    
    for i, nome in enumerate(resultados, 1):
        print(f"{i}. {nome}")