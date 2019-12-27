import pandas as pd
import random
from code.MovieData import MovieData


class RandomPredictor:
    def __init__(self, min_ocena, max_ocena):
        self.min_ocena = min_ocena
        self.max_ocena = max_ocena
        self.uim = None
        self.md = MovieData('../data/movies.dat').get_movies()

    def fit(self, X):
        self.uim = X

    def predict(self, user_id):
        user = self.uim.get_user(user_id)
        p = {}

        # for key, movie in user.iterrows():
        #     if movie["movieID"] not in p:
        #         p[movie["movieID"]] = movie["rating"]

        for key, movie in self.md.iterrows():
            if movie["id"] not in p:
                p[movie["id"]] = random.randint(self.min_ocena, self.max_ocena)

        return p
