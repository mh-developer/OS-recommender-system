import pandas as pd


class Recommender:
    def __init__(self, random_predictor):
        self.random_predictor = random_predictor

    def fit(self, X):
        pass

    def recommend(self, userID, n=10, rec_seen=True):
        pass
