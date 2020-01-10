from ctypes import py_object

import pandas as pd
import time

from code.MovieData import MovieData
import math
import random
import numpy as np


class ItemBasedPredictor:
    def __init__(self, min_values=0, threshold=0):
        self.min_values = min_values
        self.threshold = threshold
        self.uim = None
        self.md = MovieData('../data/movies.dat')
        self.movies = self.md.get_movies()
        self.p_movies = None
        self.unique_rated_movies = None

    def fit(self, X):
        self.uim = X.get_df()
        self.unique_rated_movies = pd.DataFrame(self.uim["movieID"].unique(), columns=["movieID"])
        self.unique_rated_movies = self.unique_rated_movies.set_index("movieID", drop=False)
        self.unique_rated_movies["key"] = 1
        cartesian_p = pd.merge(self.unique_rated_movies, self.unique_rated_movies, on="key")[["movieID_x", "movieID_y"]]
        cartesian_p = cartesian_p[cartesian_p["movieID_x"] != cartesian_p["movieID_y"]][["movieID_x", "movieID_y"]]
        cartesian_p["similarity"] = cartesian_p.apply(lambda x: self.similarity(x["movieID_x"], x["movieID_y"]), axis=1)
        self.p_movies = cartesian_p

    def predict(self, user_id):
        pred = {}
        user_movies = dict(self.uim.groupby(self.uim.index)['movieID'].apply(list))

        rating_movies_from_user = pd.DataFrame({'rated_movies': user_movies[user_id]})

        non_rating_movies = self.uim[~self.uim["movieID"].isin(user_movies[user_id])].drop_duplicates(subset=["movieID"])

        for key_non_rating, value_non_rating in non_rating_movies.iterrows():
            s = []
            p = []
            for key_rating, value_rating in rating_movies_from_user.iterrows():
                p1 = self.uim.loc[self.uim["movieID"] == value_rating["rated_movies"], "rating"]
                s += [self.p_movies.loc[(self.p_movies["movieID_x"] == value_non_rating["movieID"]) & (self.p_movies["movieID_y"] == value_rating["rated_movies"]), "similarity"].iat[0]]
                p += [p1[user_id]]

            if np.sum(np.array(s)) == 0:
                pred[int(value_non_rating["movieID"])] = 0.0
            else:
                pred[int(value_non_rating["movieID"])] = ((np.sum(np.array(s) * np.array(p))) / np.sum(np.array(s)))

        return pred

    def similarity(self, p1, p2):
        if p1 == p2:
            return 0.0

        # start = time.time()
        p_intersection = set(self.uim.loc[self.uim["movieID"] == p1]["userID"].unique()).intersection(set(self.uim.loc[self.uim["movieID"] == p2]["userID"].unique()))

        all_p = self.uim[self.uim["userID"].isin(p_intersection)]
        x_p1 = (all_p.loc[all_p["movieID"] == p1])
        x_p2 = (all_p.loc[all_p["movieID"] == p2])
        p1 = x_p1[x_p1["userID"].isin(p_intersection)]["rating"]
        p2 = x_p2[x_p2["userID"].isin(p_intersection)]["rating"]
        avg = (all_p.groupby(all_p.index).mean()["rating"])

        # end = time.time()
        # print(end - start)

        if max(len(p1.keys()), len(p2.keys())) < self.min_values:
            return 0.0

        c = 0
        iml = 0
        imr = 0
        for ocena_1, ocena_2, user_avg in zip(p1, p2, avg):
            c += (ocena_1 - user_avg) * (ocena_2 - user_avg)
            iml += (ocena_1 - user_avg)**2
            imr += (ocena_2 - user_avg)**2

        # end = time.time()
        # print(end - start)

        if c <= 0:
            return 0.0
        result = c / (math.sqrt(iml) * math.sqrt(imr))

        if result < self.threshold:
            return 0.0

        return result

    def mostSimilarFilms(self):
        most_similar = self.p_movies.sort_values(by='similarity', ascending=False).head(n=20)
        for key, value in most_similar.iterrows():
            print("Film1: {}, Film2: {}, podobnost: {}".format(self.md.get_title(value["movieID_x"]),
                                                               self.md.get_title(value["movieID_y"]),
                                                               value["similarity"]))

    def similarItems(self, item, n):
        films = self.uim.groupby("movieID")[["movieID"]].apply(lambda x: self.similarity(item, x.name))
        return sorted(list(dict(films).items()), key=lambda x: x[1], reverse=True)[0:n]


