import pandas as pd
import datetime
datetime.datetime.strptime


class UserItemData:
    def __init__(self, path, start_date=None, end_date=None, min_ratings=0):
        self.path = path
        self.from_date = start_date
        self.to_date = end_date
        self.min_ratings = min_ratings
        self.df = self.movies = self.read_data()

    def read_data(self):
        data = pd.read_csv(self.path, sep="\t", encoding="ISO-8859-1")
        data = data.set_index("userID", drop=False)

        if self.from_date is not None or self.to_date is not None:
            data["full_date"] = data.apply(lambda x: datetime.date(int(x['date_year']), int(x['date_month']), int(x['date_day'])), axis=1)
            data["full_date"] = pd.to_datetime(data['full_date'])

            if self.from_date is not None and self.to_date is not None:
                day, month, year = self.from_date.split(".")
                date_from = pd.Timestamp(datetime.date(int(year), int(month), int(day)))

                day, month, year = self.to_date.split(".")
                date_to = pd.Timestamp(datetime.date(int(year), int(month), int(day)))
                data = data[
                    (data['full_date'] >= date_from) &
                    (data['full_date'] < date_to)
                    ]
            elif self.from_date is not None:
                day, month, year = self.from_date.split(".")
                date_from = pd.Timestamp(datetime.date(int(year), int(month), int(day)))
                data = data[data['full_date'] >= date_from]
            elif self.to_date is not None:
                day, month, year = self.to_date.split(".")
                date_to = pd.Timestamp(datetime.date(int(year), int(month), int(day)))
                data = data[data['full_date'] < date_to]

        if self.min_ratings > 0:
            grouped = data.groupby("movieID")
            data = grouped.filter(lambda x: x["movieID"].count() > self.min_ratings)

        return data

    def nratings(self):
        return self.df.shape[0]

    def get_user(self, user_id):
        return self.df.loc[user_id]

    def head(self):
        return self.df.head()

    def get_key(self):
        return self.df.keys()

    def get_df(self):
        return self.df
