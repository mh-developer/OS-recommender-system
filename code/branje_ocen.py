from code.UserItemData import UserItemData

uim = UserItemData('../data/user_ratedmovies.dat')
print(uim.nratings())

uim = UserItemData('../data/user_ratedmovies.dat', start_date='12.1.2007', end_date='16.2.2008', min_ratings=100)
print(uim.nratings())
