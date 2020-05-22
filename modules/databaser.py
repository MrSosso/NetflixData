from modules import var
import sqlite3 as sql


class Databaser(object):
    def __init__(self):
        self.connection = sql.connect(var.NETFLIX_DATA_DATABASE)
        self.cursor = self.connection.cursor()

    def _create_table(self):
        self.cursor.execute('CREATE TABLE "ratings" ("movie_ID"	INTEGER NOT NULL, "costumer_ID"	INTEGER NOT NULL, "value"	INTEGER NOT NULL, "date"	TEXT NOT NULL);')

    def _load_ratings(self, ):
        for filepath in var.RATINGS_DATA_FILES:
            with open(filepath) as f:
                movie = None
                for line in f.readlines():
                    if ":" == line[-2]:
                        movie = int(line[:-2])
                        print(movie)
                        continue
                    raw = line[:-1].split(",")
                    costumer = int(raw[0])
                    value = int(raw[1])
                    date = raw[2]
                    self.cursor.execute("INSERT INTO ratings VALUES (?, ?, ?, ?)", (movie, costumer, value, date))
            self.connection.commit()

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()