class Costumer(object):
    def __init__(self, ID):
        self.ID = ID
        self.ratings = set()

    def add_rating(self, rating):
        self.ratings.add(rating)

    def __str__(self):
        return f"{self.ID:07d} - {len(self.ratings)} ratings"
