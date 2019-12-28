import pandas as pd
from code.MovieData import MovieData


class Recommender:
    def __init__(self, predictor):
        self.predictor = predictor
        self.uim = None
        self.md = MovieData('../data/movies.dat').get_movies()

    def fit(self, X):
        self.uim = X
        self.predictor.fit(X)

    def recommend(self, user_id, n=10, rec_seen=True):
        user = self.uim.get_user(user_id)
        pred = self.predictor.predict(user_id)

        if not rec_seen:
            for key, movie in user.iterrows():
                if movie["movieID"] in pred:
                    del pred[movie["movieID"]]

        return sorted(list(pred.items()), key=lambda x: x[1], reverse=True)[0:n]

    def evaluate(self, test_data, n):
        pass

