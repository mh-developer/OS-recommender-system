from code.MovieData import MovieData
from code.Recommender import Recommender
from code.SlopeOnePredictor import SlopeOnePredictor
from code.UserItemData import UserItemData

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
