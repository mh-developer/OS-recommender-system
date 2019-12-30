from code.AveragePredictor import AveragePredictor
from code.ItemBasedPredictor import ItemBasedPredictor
from code.MovieData import MovieData
from code.RandomPredictor import RandomPredictor
from code.Recommender import Recommender
from code.SlopeOnePredictor import SlopeOnePredictor
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


print(uim.get_df().loc[uim.get_df()["movieID"] == 1, "rating"])

# Priporočanje s povprečnim prediktorjem
print("------------------------------")
print("Priporočanje s povprečnim prediktorjem")
print("------------------------------")
ap = AveragePredictor(b=0)
rec = Recommender(ap)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

# ###
print("------------------------------")
ap = AveragePredictor(b=100)
rec = Recommender(ap)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


# Priporočanje najbolj gledanih filmov
print("------------------------------")
print("Priporočanje najbolj gledanih filmov")
print("------------------------------")
rp = ViewsPredictor()
rec = Recommender(rp)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))



# Napovedovanje ocen s podobnostjo med produkti

print("------------------------------")
print("Napovedovanje ocen s podobnostjo med produkti")
print("------------------------------")

md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat')
rp = ItemBasedPredictor()
rec = Recommender(rp)
rec.fit(uim)
print("Podobnost med filmoma 'Men in black'(1580) in 'Ghostbusters'(2716): ", rp.similarity(1580, 2716))
print("Podobnost med filmoma 'Men in black'(1580) in 'Schindler's List'(527): ", rp.similarity(1580, 527))
print("Podobnost med filmoma 'Men in black'(1580) in 'Independence day'(780): ", rp.similarity(1580, 780))

#
# print("Predictions for 78: ")
# rec_items = rec.recommend(78, n=15, rec_seen=False)
# for idmovie, val in rec_items:
#     print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))





# Najbolj podobni filmi
###



# Priporočanje glede na trenutno ogledano vsebino
rec_items = rp.similarItems(4993, 10)
print('Filmi podobni "The Lord of the Rings: The Fellowship of the Ring": ')
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


# Priporočilo zase
###


# Napovedovanje z metodo Slope one
md = MovieData('data/movies.dat')
uim = UserItemData('data/user_ratedmovies.dat', min_ratings=1000)
rp = SlopeOnePredictor()
rec = Recommender(rp)
rec.fit(uim)

print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))




# evalvacija priporočilnega sistema

md = MovieData('data/movies.dat')
uim = UserItemData('data/user_ratedmovies.dat', min_ratings=1000, end_date='1.1.2008')
rp = SlopeOnePredictor()
rec = Recommender(rp)
rec.fit(uim)

uim_test = UserItemData('data/user_ratedmovies.dat', min_ratings=200, start_date='2.1.2008')
mse, mae, precision, recall, f = rec.evaluate(uim_test, 20)
print(mse, mae, precision, recall, f)
