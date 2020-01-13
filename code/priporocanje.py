from code.AveragePredictor import AveragePredictor
from code.ItemBasedPredictor import ItemBasedPredictor
from code.MovieData import MovieData
from code.RandomPredictor import RandomPredictor
from code.Recommender import Recommender
from code.SlopeOnePredictor import SlopeOnePredictor
from code.UserItemData import UserItemData
from code.ViewsPredictor import ViewsPredictor
import pandas as pd
import time

start = time.time()

md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat')


# Priporočanje z naključnim prediktorjem
print("------------------------------")
print("Priporočanje z naključnim prediktorjem")
print("------------------------------")
rp = RandomPredictor(1, 5)
rec = Recommender(rp)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


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
uim = UserItemData('../data/user_ratedmovies.dat', min_ratings=1000)
rp = ItemBasedPredictor()
rec = Recommender(rp)
rec.fit(uim)
# print(uim.movies)
print("Podobnost med filmoma 'Men in black'(1580) in 'Ghostbusters'(2716): ", rp.similarity(1580, 2716))
print("Podobnost med filmoma 'Men in black'(1580) in 'Schindler's List'(527): ", rp.similarity(1580, 527))
print("Podobnost med filmoma 'Men in black'(1580) in 'Independence day'(780): ", rp.similarity(1580, 780))


print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))





# Najbolj podobni filmi
print("------------------------------")
print("Najbolj podobni filmi")
print("------------------------------")

rp.mostSimilarFilms()


# Priporočanje glede na trenutno ogledano vsebino
print("------------------------------")
print("Priporočanje glede na trenutno ogledano vsebino")
print("------------------------------")
rec_items = rp.similarItems(4993, 10)
print('Filmi podobni "The Lord of the Rings: The Fellowship of the Ring": ')
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


# Priporočilo zase
print("------------------------------")
print("Priporočilo zase")
print("------------------------------")

md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat', min_ratings=1000)
rp = ItemBasedPredictor()
rec = Recommender(rp)
moje_ocene = pd.DataFrame({ "userID":  [1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567, 1234567],
                            "movieID": [40815, 54001, 59315, 6564, 6537, 6539, 45722, 46530, 2571, 5507, 2378, 2379, 2380, 2381, 2382, 2383, 2393, 2402, 2404, 4277, 4638, 480, 7991, 2116, 2115, 5952, 5944, 2947, 2323, 4369],
                            "rating":  [4, 4.5, 4, 3, 4, 5, 5, 3, 3.5, 4.5, 4, 3.5, 4.5, 3, 4, 3.5, 5, 4.5, 4, 4.5, 5, 4, 5, 4.5, 5, 4, 4.5, 5, 4, 5],
                            "date_day": [11 for i in range(30)],
                            "date_month": [1 for i in range(30)],
                            "date_year": [2020 for i in range(30)],
                            "date_hour": [11 for i in range(30)],
                            "date_minute": [11 for i in range(30)],
                            "date_second": [11 for i in range(30)],
                            })
uim.df = uim.movies = uim.get_df().append(moje_ocene, ignore_index=True)
uim.df = uim.movies = uim.df.set_index("userID", drop=False)
rec.fit(uim)

print("Predictions for me 1234567: ")
rec_items = rec.recommend(1234567, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))



# Napovedovanje z metodo Slope one
print("------------------------------")
print("Napovedovanje z metodo Slope one")
print("------------------------------")
md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat', min_ratings=1000)
rp = SlopeOnePredictor()
rec = Recommender(rp)
rec.fit(uim)

print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))




# evalvacija priporočilnega sistema
print("------------------------------")
print("Evalvacija priporočilnega sistema")
print("------------------------------")

md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat', min_ratings=1000, end_date='1.1.2008')
rp = SlopeOnePredictor()
rec = Recommender(rp)
rec.fit(uim)

uim_test = UserItemData('../data/user_ratedmovies.dat', min_ratings=200, start_date='2.1.2008')
mse, mae, precision, recall, f = rec.evaluate(uim_test, 20)
print(mse, mae, precision, recall, f)

end = time.time()
print("Čas izvajanja programa: ", end - start)
