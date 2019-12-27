import pandas as pd

from code.MovieData import MovieData


class ViewsPredictor:
    def __init__(self):
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
