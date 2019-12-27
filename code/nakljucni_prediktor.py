from code.UserItemData import UserItemData
from code.MovieData import MovieData
from code.RandomPredictor import RandomPredictor
import pandas as pd

md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat')
rp = RandomPredictor(1, 5)
rp.fit(uim)
pred = rp.predict(78)
print(type(pred))
items = [1, 3, 20, 50, 100]
for item in items:
    print("Film: {}, ocena: {}".format(md.get_title(item), pred[item]))
