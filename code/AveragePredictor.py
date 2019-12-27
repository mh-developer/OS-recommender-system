import pandas as pd

from code.MovieData import MovieData


class AveragePredictor:
    def __init__(self, b):
        self.b = b
        self.uim = None
        self.md = MovieData('../data/movies.dat').get_movies()
        self.fitted = None

    def fit(self, X):
        self.uim = X.get_df()
        # avg = (vs + b * g_avg) / (n + b)
        # - vs je vsota vseh ocen za ta film,
        # - n je število ocen, ki jih je ta film dobil,
        # - g_avg je povprečje čez vse filme,
        # - b je parameter formule za povprečje. Če je b=0, gre za navadno povprečje.
        f = {}

        for key, movie in self.md.iterrows():
            if movie["id"] not in f:
                vs = sum(self.uim.loc[self.uim["movieID"] == movie["id"], "rating"])
                n = len(self.uim.loc[self.uim["movieID"] == movie["id"], "rating"])
                g_avg = sum(self.uim.loc[:, "rating"]) / len(self.uim.loc[:, "rating"])

                if n == 0:
                    n = 1

                avg = (vs + self.b * g_avg) / (n + self.b)
                f[movie["id"]] = avg

        self.fitted = f

    def predict(self, user_id):
        return self.fitted
