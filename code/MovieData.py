import pandas as pd


class MovieData:
    def __init__(self, path, from_date="", to_date=""):
        self.path = path
        self.from_date = from_date
        self.to_date = to_date
        self.df = self.read_data()

    def read_data(self):
        data = pd.read_csv(self.path, sep="\t", encoding="ISO-8859-1")
        data = data.set_index("id", drop=False)
        return data

    def get_title(self, movie_id):
        return self.df.loc[movie_id, "title"]

    def get_movie(self, movie_id):
        return self.df.loc[movie_id]

    def get_movies(self):
        return self.df
