class Rating(object):
    def __init__(self, movie, costumer, value, date):
        self.movie = movie
        self.costumer = costumer
        self.value = value
        self.date = date
        self._update_movie_and_costumer()

    def _update_movie_and_costumer(self):
        self.movie.add_rating(self)
        # self.costumer.add_rating(self)
