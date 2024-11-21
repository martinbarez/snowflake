import pickle
import sys
import pathlib

from snowflake import Automata, save_svg

size = 60
steps = 100


# create a crystal and grow it
def example_1():
    automata = Automata(size)
    automata.grow(steps)
    save_svg(automata, "examples/example_1.svg")


# create a crystal in a custom environment and grow it
def example_2():
    params = {
        "rho": 0.9,
        "beta": 1.2,
        "alpha": 0.21,
        "theta": 0.1,
        "kappa": 0.07,
        "mu": 0.015,
        "upsilon": 0.00005,
        "sigma": 0.1,
    }
    automata = Automata(size, params)
    automata.grow(steps)
    save_svg(automata, "examples/example_2.svg")


# create a crystal, grow it a bit, dump it, load it and grow it some more
def example_3():
    saved = Automata(size)
    saved.grow(steps // 2)
    with open("examples/example_3.pkl", "wb") as f:
        pickle.dump(saved, f)
    with open("examples/example_3.pkl", "rb") as f:
        loaded = pickle.load(f)
    loaded.grow(steps // 2)
    save_svg(loaded, "examples/example_3.svg")


if __name__ == "__main__":
    pathlib.Path("examples").mkdir(exist_ok=True)
    example_1()
    example_2()
    example_3()
