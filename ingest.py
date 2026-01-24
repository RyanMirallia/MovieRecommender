import pandas as pd
import os
from sqlalchemy import create_engine

df = pd.read_csv('data/netflix_titles.csv')

INPUT_PATH = os.path.join('data', 'netflix_titles.csv')
OUTPUT_PATH = os.path.join('data', 'netflix_titles_cleaned.csv')
DB_PATH = 'sqlite:///' + os.path.join('data', 'netflix.db')

def processa_dados():

    if not os.path.exists(INPUT_PATH):
        print(f"file {INPUT_PATH} not found!")
        return
        
    df = pd.read_csv(INPUT_PATH)

    #clear null values 

    df['director'] = df['director'].fillna('Not Listed')
    df['cast'] = df['cast'].fillna('Unknown Cast')
    df['country'] = df['country'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('NR')

    df = df.dropna(subset=['duration', 'date_added'])

    #the date_added columns data types defined as date_time 

    df['date_added'] = pd.to_datetime(df['date_added'].str.strip())

    engine = create_engine(DB_PATH)

    df.to_sql('titles', con=engine, if_exists='replace', index=False)
    print(f"db updated path: {DB_PATH}")

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"file clear and saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    processa_dados()

