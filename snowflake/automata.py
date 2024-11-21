import random


class Automata(object):
    def __init__(self, size, params=None):
        self.size = size
        self.iteration = 0
        if params is not None:
            self.params = params
        else:
            self.params = {
                "rho": 0.64,
                "beta": 1.6,
                "alpha": 0.21,
                "theta": 0.0205,
                "kappa": 0.07,
                "mu": 0.015,
                "upsilon": 0.00005,
                "sigma": 0.0,
            }
        self.cells = [None] * (self.size * self.size)
        self.init_cells()

    # remove cycles for pickling
    def __getstate__(self):
        for cell in self.cells:
            cell.neighbours = None
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict
        for y in range(self.size):
            for x in range(self.size):
                self.cells[self._index(x, y)].neighbours = list(self._gen_neighbours(x, y))

    def _index(self, x, y):
        return y * self.size + x

    def _inside(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def _gen_neighbours(self, x, y):
        # https://www.redblobgames.com/grids/hexagons/#coordinates-offset
        odd_q = [
            [(x+1,y  ), (x+1,y-1), (x  ,y-1), (x-1,y-1), (x-1,y  ), (x,y+1)],# even rows
            [(x+1,y+1), (x+1,y  ), (x  ,y-1), (x-1,y  ), (x-1,y+1), (x,y+1)]] # odd rows
        inside = filter(lambda x: self._inside(x[0], x[1]), odd_q[x%2])
        index = map(lambda x: self._index(x[0], x[1]), inside)
        return (self.cells[i] for i in index)  # generator

    def init_cells(self):
        for y in range(self.size):
            for x in range(self.size):
                self.cells[self._index(x, y)] = Cell(self.params, self._gen_neighbours(x, y))

        # seed crystal
        center = self._index(self.size // 2, self.size // 2)
        self.cells[center].attach()
        self.cells[center].crystal_mass = 1

        for cell in self.cells:
            cell.neighbours = list(cell.neighbours)  # generate
            cell.update_boundaries()

    # grow n steps or until margin is reached
    def grow(self, steps=50, margin=10):
        while steps > 0 and self._headroom(margin):
            self.step()
            self.iteration += 1
            steps -= 1

    def _headroom(self, margin):
        i = 0
        while self.cells[self._index(self.size//2, self.size//2-i)].attached:
            i += 1
        return i < self.size - margin

    def step(self):
        for cell in self.cells:
            cell.diffusion()
        for cell in self.cells:
            cell.freezing()
        for cell in self.cells:
            cell.attachment()
        for cell in self.cells:
            cell.update_boundaries()
            cell.melting()
            cell.noise()


# MODELING SNOW CRYSTAL GROWTH II
# Gravner, Griffeath
class Cell(object):
    def __init__(self, params, neighbours):
        self.params = params
        self.boundary_mass = 0.0  # b // quasi-liquid
        self.crystal_mass = 0.0  # c // ice
        self.diffusive_mass = params["rho"]  # d // vapor
        self.attached = False  # a // solid
        self.boundary = False  # liquid next to solid
        self.attached_neighbours = 0
        self.neighbours = neighbours

    def update_boundaries(self):
        if not self.attached:
            self.attached_neighbours = sum([cell.attached for cell in self.neighbours])
            self.boundary = self.attached_neighbours >= 1

    def attach(self):
        self.crystal_mass = self.boundary_mass + self.crystal_mass
        self.boundary_mass = 0
        self.attached = True
        self.boundary = False

    # 1
    def diffusion(self):
        self._next_dm = self.diffusive_mass
        if not self.attached:
            for cell in self.neighbours:
                if cell.attached:
                    # Reflecting boundary conditions are used at the edge of the crystal
                    self._next_dm += self.diffusive_mass
                else:
                    self._next_dm += cell.diffusive_mass
            self._next_dm = self._next_dm / (len(self.neighbours) + 1)

    # 2
    def freezing(self):
        self.diffusive_mass = self._next_dm
        if self.boundary:
            self.boundary_mass += (1 - self.params["kappa"]) * self.diffusive_mass
            self.crystal_mass += self.params["kappa"] * self.diffusive_mass
            self.diffusive_mass = 0

    # 3
    def attachment(self):
        if self.boundary:
            if self.attached_neighbours <= 2:
                if self.boundary_mass >= self.params["beta"]:
                    self.attach()
            elif self.attached_neighbours == 3:
                if self.boundary_mass >= 1:
                    self.attach()
                else:
                    summed_diffusion = self.diffusive_mass
                    for cell in self.neighbours:
                        summed_diffusion += cell.diffusive_mass
                    if summed_diffusion < self.params["theta"] and self.boundary_mass >= self.params["alpha"]:
                        self.attach()
            elif self.attached_neighbours >= 4:
                self.attach()

    # 4
    def melting(self):
        if self.boundary:
            self.diffusive_mass += self.params["mu"] * self.boundary_mass + self.params["upsilon"] * self.crystal_mass
            self.boundary_mass = (1 - self.params["mu"]) * self.boundary_mass
            self.crystal_mass = (1 - self.params["upsilon"]) * self.crystal_mass

    # 5
    def noise(self):
        if not self.attached:
            if random.random() >= 0.5:
                self.diffusive_mass = (1 - self.params["sigma"]) * self.diffusive_mass
            else:
                self.diffusive_mass = (1 + self.params["sigma"]) * self.diffusive_mass
