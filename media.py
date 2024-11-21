import pickle
import sys
from pathlib import Path
from multiprocessing import Process

from snowflake import Automata, save_svg


# https://stackoverflow.com/a/15801617
def drawProgressBar(percent, barLen=60):
    sys.stdout.write("\r")
    sys.stdout.write(
        "[{:<{}}] {:.0f}%".format("=" * int(barLen * percent), barLen, percent * 100)
    )
    sys.stdout.flush()


size = 512
steps = 5000

figures = [
          #("02tr", {"rho" : 0.8,   "beta" : 2.9,  "alpha" : 0.006, "theta" : 0.004,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0.00002}),
           ("02br", {"rho" : 0.64,  "beta" : 1.6,  "alpha" : 0.21,  "theta" : 0.0205, "kappa" : 0.07,   "mu" : 0.015, "upsilon" : 0.00005,  "sigma" : 0}),
           ("04",   {"rho" : 0.58,  "beta" : 3.2,  "alpha" : 0,     "theta" : 0,      "kappa" : 0,      "mu" : 0,     "upsilon" : 0,        "sigma" : 0}),
          #("06b",  {"rho" : 0.8,   "beta" : 2.6,  "alpha" : 0,     "theta" : 0,      "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0.00005}),
           ("09tl", {"rho" : 0.40,  "beta" : 1.3,  "alpha" : 0.08,  "theta" : 0.025,  "kappa" : 0.003,  "mu" : 0.07,  "upsilon" : 0.00005,  "sigma" : 0}),
           ("09tm", {"rho" : 0.41,  "beta" : 1.3,  "alpha" : 0.08,  "theta" : 0.025,  "kappa" : 0.003,  "mu" : 0.07,  "upsilon" : 0.00005,  "sigma" : 0}),
           ("09tr", {"rho" : 0.42,  "beta" : 1.3,  "alpha" : 0.08,  "theta" : 0.025,  "kappa" : 0.003,  "mu" : 0.07,  "upsilon" : 0.00005,  "sigma" : 0}),
           ("09bl", {"rho" : 0.44,  "beta" : 1.3,  "alpha" : 0.08,  "theta" : 0.025,  "kappa" : 0.003,  "mu" : 0.07,  "upsilon" : 0.00005,  "sigma" : 0}),
           ("09bm", {"rho" : 0.46,  "beta" : 1.3,  "alpha" : 0.08,  "theta" : 0.025,  "kappa" : 0.003,  "mu" : 0.07,  "upsilon" : 0.00005,  "sigma" : 0}),
           ("09br", {"rho" : 0.50,  "beta" : 1.3,  "alpha" : 0.08,  "theta" : 0.025,  "kappa" : 0.003,  "mu" : 0.07,  "upsilon" : 0.00005,  "sigma" : 0}),
           ("10tl", {"rho" : 0.8,   "beta" : 1.9,  "alpha" : 0.004, "theta" : 0.001,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0}),
           ("10tm", {"rho" : 0.8,   "beta" : 2.2,  "alpha" : 0.004, "theta" : 0.001,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0}),
           ("10tr", {"rho" : 0.8,   "beta" : 2.4,  "alpha" : 0.004, "theta" : 0.001,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0}),
           ("10bl", {"rho" : 0.8,   "beta" : 2.6,  "alpha" : 0.004, "theta" : 0.001,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0}),
           ("10bm", {"rho" : 0.8,   "beta" : 2.7,  "alpha" : 0.004, "theta" : 0.001,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0}),
           ("10br", {"rho" : 0.8,   "beta" : 2.8,  "alpha" : 0.004, "theta" : 0.001,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0}),
           ("11tl", {"rho" : 0.635, "beta" : 1.6,  "alpha" : 0.4,   "theta" : 0.025,  "kappa" : 0.001,  "mu" : 0.015, "upsilon" : 0.0005,   "sigma" : 0}),
           ("11tm", {"rho" : 0.635, "beta" : 1.6,  "alpha" : 0.4,   "theta" : 0.025,  "kappa" : 0.0025, "mu" : 0.015, "upsilon" : 0.0005,   "sigma" : 0}),
           ("11tr", {"rho" : 0.635, "beta" : 1.6,  "alpha" : 0.4,   "theta" : 0.025,  "kappa" : 0.005,  "mu" : 0.015, "upsilon" : 0.0005,   "sigma" : 0}),
           ("11bl", {"rho" : 0.635, "beta" : 1.6,  "alpha" : 0.4,   "theta" : 0.025,  "kappa" : 0.0075, "mu" : 0.015, "upsilon" : 0.0005,   "sigma" : 0}),
           ("11bm", {"rho" : 0.635, "beta" : 1.6,  "alpha" : 0.4,   "theta" : 0.025,  "kappa" : 0.01,   "mu" : 0.015, "upsilon" : 0.0005,   "sigma" : 0}),
           ("11br", {"rho" : 0.635, "beta" : 1.6,  "alpha" : 0.4,   "theta" : 0.025,  "kappa" : 0.02,   "mu" : 0.015, "upsilon" : 0.0005,   "sigma" : 0}),
           ("12tl", {"rho" : 0.5,   "beta" : 1.4,  "alpha" : 0.1,   "theta" : 0.005,  "kappa" : 0.001,  "mu" : 0.04,  "upsilon" : 0.001,    "sigma" : 0}),
           ("12tm", {"rho" : 0.5,   "beta" : 1.4,  "alpha" : 0.1,   "theta" : 0.005,  "kappa" : 0.001,  "mu" : 0.05,  "upsilon" : 0.001,    "sigma" : 0}),
           ("12tr", {"rho" : 0.5,   "beta" : 1.4,  "alpha" : 0.1,   "theta" : 0.005,  "kappa" : 0.001,  "mu" : 0.06,  "upsilon" : 0.001,    "sigma" : 0}),
           ("12bl", {"rho" : 0.5,   "beta" : 1.4,  "alpha" : 0.1,   "theta" : 0.005,  "kappa" : 0.001,  "mu" : 0.07,  "upsilon" : 0.001,    "sigma" : 0}),
           ("12bm", {"rho" : 0.5,   "beta" : 1.4,  "alpha" : 0.1,   "theta" : 0.005,  "kappa" : 0.001,  "mu" : 0.08,  "upsilon" : 0.001,    "sigma" : 0}),
           ("12br", {"rho" : 0.5,   "beta" : 1.4,  "alpha" : 0.1,   "theta" : 0.005,  "kappa" : 0.001,  "mu" : 0.09,  "upsilon" : 0.001,    "sigma" : 0}),
           ("13l",  {"rho" : 0.65,  "beta" : 1.75, "alpha" : 0.2,   "theta" : 0.026,  "kappa" : 0.15,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0}),
           ("13m",  {"rho" : 0.36,  "beta" : 1.09, "alpha" : 0.01,  "theta" : 0.0745, "kappa" : 0.0001, "mu" : 0.14,  "upsilon" : 0.00001,  "sigma" : 0}),
           ("13r",  {"rho" : 0.38,  "beta" : 1.06, "alpha" : 0.35,  "theta" : 0.112,  "kappa" : 0.001,  "mu" : 0.14,  "upsilon" : 0.0006,   "sigma" : 0}),
           ("14r",  {"rho" : 0.37,  "beta" : 1.09, "alpha" : 0.02,  "theta" : 0.09,   "kappa" : 0.003,  "mu" : 0.12,  "upsilon" : 0.000001, "sigma" : 0}),
          #("15tl", {"rho" : 0.65,  "beta" : 1.8,  "alpha" : 0.6,   "theta" : 0.067,  "kappa" : 0.001,  "mu" : 0.05,  "upsilon" : 0.0005,   "sigma" : 0.00002}),
          #("15tm", {"rho" : 0.35,  "beta" : 1.4,  "alpha" : 0.001, "theta" : 0.015,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.01,     "sigma" : 0.00005}),
          #("15tr", {"rho" : 0.5,   "beta" : 1.3,  "alpha" : 0.08,  "theta" : 0.025,  "kappa" : 0.003,  "mu" : 0.07,  "upsilon" : 0.00005,  "sigma" : 0.00001}),
          #("15bl", {"rho" : 0.66,  "beta" : 1.6,  "alpha" : 0.4,   "theta" : 0.025,  "kappa" : 0.075,  "mu" : 0.015, "upsilon" : 0.00005,  "sigma" : 0}),
          #("15bm", {"rho" : 0.65,  "beta" : 1.75, "alpha" : 0.2,   "theta" : 0.026,  "kappa" : 0.15,   "mu" : 0.015, "upsilon" : 0.00001,  "sigma" : 0}),
          #("15br", {"rho" : 0.6,   "beta" : 1.3,  "alpha" : 0.3,   "theta" : 0.1,    "kappa" : 0.0001, "mu" : 0.1,   "upsilon" : 0.0001,   "sigma" : 0}),
           ("16l",  {"rho" : 0.66,  "beta" : 1.6,  "alpha" : 0.4,   "theta" : 0.025,  "kappa" : 0.075,  "mu" : 0.015, "upsilon" : 0.00005,  "sigma" : 0.000006}),
           ("16m",  {"rho" : 0.65,  "beta" : 2.6,  "alpha" : 0.2,   "theta" : 0.0245, "kappa" : 0.1,    "mu" : 0.015, "upsilon" : 0.00005,  "sigma" : 0.00001}),
           ("16r",  {"rho" : 0.8,   "beta" : 2.6,  "alpha" : 0.006, "theta" : 0.005,  "kappa" : 0.05,   "mu" : 0.015, "upsilon" : 0.0001,   "sigma" : 0.00005})
          #("17m",  {"rho" : 0.58,  "beta" : 2,    "alpha" : 0.8,   "theta" : 0.011,  "kappa" : 0.1,    "mu" : 0.01,  "upsilon" : 0.00005,  "sigma" : 0}),
          #("17r",  {"rho" : 0.58,  "beta" : 3,    "alpha" : 0.4,   "theta" : 0.02,   "kappa" : 0.1,    "mu" : 0.01,  "upsilon" : 0.00005,  "sigma" : 0})
]


def task(name, params):
    with open(f"media/{name}.pkl", "rb") as f:
        automata = pickle.load(f)
        save_svg(automata, f"media/{name}.svg")


if __name__ == "__main__":
    Path("media").mkdir(exist_ok=True)
    tasklist = []
    for name, params in figures:
        tasklist.append(Process(target=task, args=(name, params)))
    for t in tasklist:
        t.start()
    for t in tasklist:
        t.join()
    print()
