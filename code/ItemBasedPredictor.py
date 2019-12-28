import pandas as pd

from code.MovieData import MovieData


class ItemBasedPredictor:
    def __init__(self, min_values=0, threshold=0):
        self.min_values = min_values
        self.threshold = threshold
        self.uim = None
        self.md = MovieData('../data/movies.dat').get_movies()

    def fit(self, X):
        self.uim = X.get_df()

    def predict(self, user_id):
        pred = {}

        for key, movie in self.md.iterrows():
            if movie["id"] not in pred:
                pred[movie["id"]] = len(self.uim.loc[self.uim["movieID"] == movie["id"]])

        return pred

    def similarity(self, p1, p2):
        pass

    def similarItems(self, item, n):
        pass

