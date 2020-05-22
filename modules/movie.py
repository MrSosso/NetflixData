from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from modules import var
import numpy as np
import os, datetime


class Movie(object):
    def __init__(self, ID, year, title):
        self.ID = ID
        self.year = year
        self.title = title
        self.ratings = set()

    def add_rating(self, rating):
        self.ratings.add(rating)

    def generate_scatter_diagram(self):
        x, y = zip(*((i.date, i.value) for i in self.ratings))
        date_range = (min(x), var.DATE_RANGE[1])
        average = sum(y) / len(y)
        plt.figure(figsize=(12, 3))
        plt.scatter(x, y, s=1, marker=",")
        plt.hlines(average, xmin=date_range[0], xmax=date_range[1], color="red", linestyles="dashed", linewidth=2)
        plt.text(date_range[0], average - 0.4, f'  {average:.02f}', color="red")
        plt.xlabel("Date")
        plt.ylabel("Rating")
        plt.title(str(self))
        plt.ylim(0.5, 5.5)
        plt.xlim(date_range)
        plt.tick_params(axis='both', labelsize=8)
        plt.tight_layout()
        plt.savefig(os.path.join(var.DIAGRAMS_DIR, "scatter", f"scatter_movie_{self.ID:05d}.png"), dpi=300)
        plt.close()

    def generate_monthly_ratings_diagram(self):
        data = dict()
        for i in self.ratings:
            try:
                data[datetime.datetime(i.date.year, i.date.month, 1)] += 1
            except KeyError:
                data[datetime.datetime(i.date.year, i.date.month, 1)] = 1
        x, y = zip(*sorted(data.items()))
        date_range = (min(x), var.DATE_RANGE[1])
        average = sum(y) / len(y)
        plt.plot(x, y, color="darkgray")
        plt.hlines(average, xmin=date_range[0], xmax=date_range[1], color="gray", linestyles="dashed", linewidth=2)
        plt.text(date_range[0], average, f'  {round(average)}', color="gray", verticalalignment="bottom")
        plt.xlabel("Month")
        plt.ylabel("Monthly ratings")
        plt.title(str(self))
        plt.xlim(date_range)
        plt.tick_params(axis='both', labelsize=8)
        plt.tight_layout()
        plt.savefig(os.path.join(var.DIAGRAMS_DIR, "monthly", f"monthly_movie_{self.ID:05d}.png"), dpi=300)
        plt.close()

    def generate_moving_distribution_diagram(self, norm=False):

        dates = tuple(i.date for i in self.ratings)
        date_range = (min(dates), var.DATE_RANGE[1])
        Z = list(list() for i in range(5))
        Av = list()
        day = date_range[0] + var.MOVING_ANALYSIS_DATE_RANGE
        while True:
            ratings = tuple(filter(lambda x: day - var.MOVING_ANALYSIS_DATE_RANGE <= x.date <= day + var.MOVING_ANALYSIS_DATE_RANGE, self.ratings))
            expect_val = 0
            for i in range(5):
                val = len(tuple(filter(lambda x: x.value == i + 1, ratings)))
                expect_val += (i + 1) * val
                if norm:
                    try:
                        val = val / len(ratings)
                    except ZeroDivisionError:
                        val = 0
                Z[i].append(val)

            try:
                Av.append(expect_val / len(ratings))
            except ZeroDivisionError:
                Av.append(Av[-1])

            if day == date_range[1] - var.MOVING_ANALYSIS_DATE_RANGE:
                break
            day += var.MOVING_ANALYSIS_DATE_INCREASE

        tot_days = len(Z[0])
        y = np.linspace(0, tot_days - 1, tot_days)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim(5.5, 0.5)
        ax.set_ylim(0, tot_days - 1)

        polys = list()
        for i in range(5):
            polys.append([(0, 0), *zip(y, Z[i]), (tot_days - 1, 0.)])
        poly = PolyCollection(polys, facecolors=var.RATINGS_COLORS, alpha=.6)
        ax.add_collection3d(poly, zs=range(1, 6), zdir='x')

        for i in range(4, -1, -1):
            plt.plot((i + 1,) * tot_days, y, Z[i], color=var.RATINGS_COLORS[i], linewidth=3)

        ax.plot(Av, y, (0,) * tot_days, color="red", linewidth=2)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Day")
        ax.set_zlabel("# of votes")
        ax.set_title(str(self))

        plt.tight_layout()
        plt.savefig(os.path.join(var.DIAGRAMS_DIR, f"{'relative_' if norm else ''}moving_distribution", f"{'relative_' if norm else ''}moving_distribution_movie_{self.ID:05d}.png"), dpi=300)
        plt.close()

    def generate_month_distribution_diagram(self, norm=False):

        dates = tuple(i.date for i in self.ratings)
        date_range = (min(dates), var.DATE_RANGE[1])
        Z = list(list() for i in range(5))
        Av = list()
        year = date_range[0].year
        month = date_range[0].month
        while True:
            ratings = tuple(filter(lambda x: x.date.year == year and x.date.month == month, self.ratings))
            expect_val = 0
            for i in range(5):
                val = len(tuple(filter(lambda x: x.value == i + 1, ratings)))
                expect_val += (i + 1) * val
                if norm:
                    try:
                        val = val / len(ratings)
                    except ZeroDivisionError:
                        val = 0
                Z[i].append(val)

            try:
                Av.append(expect_val / len(ratings))
            except ZeroDivisionError:
                Av.append(Av[-1])

            if year >= date_range[1].year and month >= date_range[1].month:
                break
            month += 1
            if month > 12:
                month = 1
                year += 1

        tot_months = len(Z[0])
        y = np.linspace(0, tot_months - 1, tot_months)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim(5.5, 0.5)
        ax.set_ylim(0, tot_months - 1)

        polys = list()
        for i in range(5):
            polys.append([(0, 0), *zip(y, Z[i]), (tot_months - 1, 0.)])
        poly = PolyCollection(polys, facecolors=var.RATINGS_COLORS, alpha=.6)
        ax.add_collection3d(poly, zs=range(1, 6), zdir='x')

        for i in range(4, -1, -1):
            plt.plot((i + 1,) * tot_months, y, Z[i], color=var.RATINGS_COLORS[i], linewidth=3)

        ax.plot(Av, y, (0,) * tot_months, color="red", linewidth=2)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Month")
        ax.set_zlabel("# of votes")
        ax.set_title(str(self))

        plt.tight_layout()
        plt.savefig(os.path.join(var.DIAGRAMS_DIR, f"{'relative_' if norm else ''}month_distribution", f"{'relative_' if norm else ''}month_distribution_movie_{self.ID:05d}.png"), dpi=300)
        plt.close()

    def __str__(self):
        return f"{self.ID:05d} - {self.title} ({self.year})"
