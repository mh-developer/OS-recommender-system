import pandas as pd


class MovieData:
    def __init__(self, path, from_date="", to_date=""):
        self.path = path
        self.from_date = from_date
        self.to_date = to_date
        self.df = pd.read_csv(path, sep="\t", encoding="ISO-8859-1")

    def get_title(self, param):
        pass
