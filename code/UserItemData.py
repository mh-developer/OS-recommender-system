import pandas as pd


class UserItemData:
    def __init__(self, path, from_date=None, end_date=None, min_ratings=-1):
        self.path = path
        self.from_date = from_date
        self.to_date = end_date
        self.min_ratings = min_ratings
        self.df = self.read_data()

    def read_data(self):
        if self.from_date is not None and self.to_date is not None:
            data = pd.read_csv(self.path, sep="\t", encoding="ISO-8859-1")
            mask = (pd.to_datetime("{}.{}.{}".format(data['date_day'], data['date_month'], data['date_year'])) > pd.to_datetime(self.from_date)) & \
                   (pd.to_datetime("{}.{}.{}".format(data['date_day'], data['date_month'], data['date_year'])) <= pd.to_datetime(self.to_date))

            return data.loc[mask]

        elif self.from_date is not None:
            return pd.read_csv(self.path, sep="\t", encoding="ISO-8859-1")

        elif self.to_date is not None:
            return pd.read_csv(self.path, sep="\t", encoding="ISO-8859-1")

        data = pd.read_csv(self.path, sep="\t", encoding="ISO-8859-1")
        data = data.set_index("userID", drop=False)
        return data

    def nratings(self):
        print()
        return self.df.shape[0]

    def get_user(self, user_id):
        return self.df.loc[user_id]

    def head(self):
        return self.df.head()

    def get_key(self):
        return self.df.keys()

    def get_df(self):
        return self.df
