import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.vectorizer = TfidfVectorizer()
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect('portfolio.db')
        self.data.to_sql('portfolio', conn, if_exists='replace', index=False)
        conn.close()

    def load_portfolio(self):
        # Transform techstack texts to vectors
        self.vectors = self.vectorizer.fit_transform(self.data['Techstack'])

    def query_links(self, skills):
        # Transform query skills to vector
        query_vec = self.vectorizer.transform([skills])

        # Calculate similarities
        similarities = cosine_similarity(query_vec, self.vectors)

        # Get top 2 most similar indices
        top_indices = similarities[0].argsort()[-2:][::-1]

        # Get corresponding links
        results = [{"links": self.data.iloc[idx]['Links']} for idx in top_indices]
        return results
