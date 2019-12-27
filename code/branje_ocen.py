from code.UserItemData import UserItemData
import pandas as pd

uim = UserItemData('../data/user_ratedmovies.dat')
print(uim.nratings())
# print(uim.head())

df = UserItemData('../data/user_ratedmovies.dat').get_df()
print(df.loc[df["movieID"] == 75, "rating"])

# uim = UserItemData('../data/user_ratedmovies.dat', from_date='12.1.2007', end_date='16.2.2008', min_ratings=100)
# print(uim.nratings())
