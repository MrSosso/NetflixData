from modules import var
from modules.movie import Movie
from modules.costumer import Costumer
from modules.rating import Rating
from modules.databaser import Databaser
import datetime


class NetflixData(object):
    def __init__(self):
        self.databaser = Databaser()
        self.movies = list()
        self._load_movies()
        self.costumers = set()
        self._load_ratings()

    def _load_movies(self):
        with open(var.MOVIE_TITLES_FILE, encoding='iso-8859-1') as f:
            for line in f.readlines():
                raw = line[:-1].split(",")
                try:
                    self.movies.append(Movie(int(raw[0]), int(raw[1]), "".join(raw[2:])))
                except ValueError:
                    self.movies.append(Movie(int(raw[0]), None, "".join(raw[2:])))

    def _load_ratings(self):
        for filepath in var.RATINGS_DATA_FILES:
            with open(filepath) as f:
                movie = None
                for line in f.readlines():
                    if ":" == line[-2]:
                        movie_ID = int(line[:-2])
                        if movie_ID > 1:
                            movie.generate_moving_distribution_diagram(True)
                            self.movies.pop(0)
                            # return
                        if movie_ID > 128:
                            return
                        movie = self.movies[0]
                        print(movie.ID)
                        continue
                    raw = line[:-1].split(",")
                    cost_ID = int(raw[0])
                    value = int(raw[1])
                    date = datetime.datetime.strptime(raw[2], var.DATE_FORMAT)
                    # try:
                    #     for cost in self.costumers:
                    #         if cost.ID == cost_ID:
                    #             costumer = cost
                    #             raise StopIteration
                    # except StopIteration:
                    #     pass
                    # else:
                    #     costumer = Costumer(cost_ID)
                    #     self.costumers.add(costumer)

                    Rating(movie, cost_ID, value, date)
        # movie.generate_scatter_diagram()

    def run(self):
        pass
        # for i in self.movies:
        #     print(i)
