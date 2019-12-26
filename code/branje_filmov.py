from code.MovieData import MovieData
import pandas as pd

md = MovieData('../data/movies.dat')
print(md.get_title(1))
