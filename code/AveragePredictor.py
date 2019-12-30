import pandas as pd

from code.MovieData import MovieData
import numpy as np


class AveragePredictor:
    def __init__(self, b):
        self.b = b
        self.uim = None
        self.md = MovieData('../data/movies.dat').get_movies()
        self.fitted = {}

    def fit(self, X):
        self.uim = X.get_df()

    def predict(self, user_id):
        # avg = (vs + b * g_avg) / (n + b)
        # - vs je vsota vseh ocen za ta film,
        # - n je število ocen, ki jih je ta film dobil,
        # - g_avg je povprečje čez vse filme,
        # - b je parameter formule za povprečje. Če je b=0, gre za navadno povprečje.

        vs = self.uim.groupby("movieID").sum()["rating"]
        n = self.uim.groupby("movieID").count()["rating"]
        g_avg = sum(self.uim.loc[:, "rating"]) / len(self.uim.loc[:, "rating"])

        avg = (vs + self.b * g_avg) / (n + self.b)

        self.fitted = dict(avg)
        return self.fitted
