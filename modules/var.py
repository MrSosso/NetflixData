import os
import datetime

# DIRECTORIES
DATA_DIR = os.path.join(os.getcwd(), "data")
DIAGRAMS_DIR = os.path.join(DATA_DIR, "diagrams")

# FILES
MOVIE_TITLES_FILE = os.path.join(DATA_DIR, "movie_titles.csv")
RATINGS_DATA_FILES = tuple(os.path.join(DATA_DIR, f"combined_data_{i}.txt") for i in range(1, 5))
NETFLIX_DATA_DATABASE = os.path.join(DATA_DIR, "netflix_data.nddb")

DATE_FORMAT = "%Y-%m-%d"
DATE_RANGE = (datetime.datetime(1999, 11, 11), datetime.datetime(2005, 12, 31))
MOVING_ANALYSIS_DATE_RANGE = datetime.timedelta(60)
MOVING_ANALYSIS_DATE_INCREASE = datetime.timedelta(1)

RATINGS_COLORS = ((0.16470588, 0.1372549, 0.04313725),
                  (0.32941176, 0.2745098, 0.08627451),
                  (0.49803922, 0.41176471, 0.12941176),
                  (0.66666667, 0.54901961, 0.17254902),
                  (0.83137255, 0.68627451, 0.21568627))
