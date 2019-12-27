from code.AveragePredictor import AveragePredictor
from code.MovieData import MovieData
from code.RandomPredictor import RandomPredictor
from code.Recommender import Recommender
from code.UserItemData import UserItemData
from code.ViewsPredictor import ViewsPredictor

md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat')


# Priporočanje z naključnim prediktorjem
rp = RandomPredictor(1, 5)
rec = Recommender(rp)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


# Priporočanje s povprečnim prediktorjem
# print("------------------------------")
# ap = AveragePredictor(b=0)
# rec = Recommender(ap)
# rec.fit(uim)
# rec_items = rec.recommend(78, n=5, rec_seen=False)
# for idmovie, val in rec_items:
#     print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))
#
# ###
# ap = AveragePredictor(b=100)
# rec = Recommender(ap)
# rec.fit(uim)
# rec_items = rec.recommend(78, n=5, rec_seen=False)
# for idmovie, val in rec_items:
#     print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


# Priporočanje najbolj gledanih filmov
print("------------------------------")
rp = ViewsPredictor()
rec = Recommender(rp)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


