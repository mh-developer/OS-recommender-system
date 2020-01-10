from code.MovieData import MovieData
import pandas as pd
import numpy as np


class SlopeOnePredictor:
    def __init__(self):
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
        cartesian_p["similarity_d"] = cartesian_p.apply(lambda x: self.similar_d(x["movieID_x"], x["movieID_y"]), axis=1)
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
                calculated_d = self.p_movies.loc[(self.p_movies["movieID_x"] == value_non_rating["movieID"]) & (self.p_movies["movieID_y"] == value_rating["rated_movies"]), "similarity_d"].iat[0]
                s += [(p1[user_id] - calculated_d[0])]
                p += [calculated_d[1]]

            if np.sum(np.array(p)) == 0:
                pred[int(value_non_rating["movieID"])] = 0.0
            else:
                pred[int(value_non_rating["movieID"])] = ((np.sum(np.array(s) * np.array(p))) / np.sum(np.array(p)))

        return pred

    def similar_d(self, p1, p2):
        p_intersection = set(self.uim.loc[self.uim["movieID"] == p1]["userID"].unique()).intersection(
                         set(self.uim.loc[self.uim["movieID"] == p2]["userID"].unique()))

        all_p = self.uim[self.uim["userID"].isin(p_intersection)]
        x_p1 = (all_p.loc[all_p["movieID"] == p1])
        x_p2 = (all_p.loc[all_p["movieID"] == p2])
        p1 = x_p1[x_p1["userID"].isin(p_intersection)][["movieID", "rating"]]
        p2 = x_p2[x_p2["userID"].isin(p_intersection)][["movieID", "rating"]]

        concated_movies_rating = pd.concat([p1, p2], axis=1)
        concated_movies_rating.columns = ["movieID_x", "rating_x", "movieID_y", "rating_y"]
        concated_movies_rating["calculated_d"] = concated_movies_rating.apply(lambda x: x["rating_x"] - x["rating_y"], axis=1)

        return tuple((-(concated_movies_rating["calculated_d"].sum() / concated_movies_rating["calculated_d"].count()),
                     concated_movies_rating["calculated_d"].count()))





