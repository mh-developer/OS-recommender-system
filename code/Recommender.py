from code.MovieData import MovieData
import pandas as pd
import numpy as np
import time


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
        print("Računanje evaluate")
        data = test_data.get_df()
        print(data)
        start = time.time()
        predictions = pd.DataFrame(data["userID"].unique(), columns=["userID"])
        predictions["predict"] = predictions.apply(lambda x: list(self.predictor.predict(x["userID"]).items()), axis=1)
        predictions["count"] = predictions.apply(lambda x: len(x["predict"]), axis=1)
        predictions["mae"] = predictions.apply(lambda x: self.calculate_mae(x["predict"], data.loc[data["userID"] == x["userID"]]), axis=1)
        # for key, value in predictions.iterrows():
        #     print(self.predictor.predict(value["userID"]))
        print(predictions)
        end = time.time()
        print(end - start)

        return predictions["mae"].sum() / predictions["count"].sum(), 0, 0, 0, 0

    def calculate_mae(self, movies, real_ratings):
        movies = dict(movies)
        if not movies:
            return 0.0

        if not real_ratings.bool():
            return 0.0

        print(movies)
        print(real_ratings)
        r = []
        for k, v in movies.items():
            ocena = real_ratings.loc[real_ratings["movieID"] == k, "rating"].iat[0]
            print(ocena)
            r += abs(ocena - v)
        return np.sum(np.array(r))
