import numpy as np

class Particles:

    def __init__(self, gameScreen, startColor=None, endColor=None, shape=None,
                 rate=0.5, count=100, endSize=0.01, sizeDecrease=0.95, colorFade=0.05):
        if not endColor:
            self.endColor = [1, 1, 1, 1]
        else:
            self.endColor = endColor

        if not startColor:
            self.startColor = [1, 1, 1, 1]
        else:
            self.startColor = startColor

        if not shape:
            self.shape = [[0, 0], [0.05, 0], [0.05, -0.05], [0, -0.05]]
        else:
            self.shape = shape

        self.gameScreen = gameScreen
        self.particles = []
        self.rate = rate
        self.count = count
        self.endSize = endSize
        self.sizeDecrease = sizeDecrease
        self.colorFade = colorFade
        self.time = 0

    def update(self):
        toRemove = []
        for particle in self.particles:
            if abs(particle[1][0][0] - particle[1][1][0]) < self.endSize:
                toRemove.append(particle)

            shape = []
            for vert in particle[1]:
                shape.append([vert[0] * self.sizeDecrease, vert[1] * self.sizeDecrease])
            particle[1] = shape
            particle[2] = self.getColor(particle[-1])
            particle[-1] -= self.colorFade
            self.gameScreen.renderInfoList.append(particle)

        for particle in toRemove:
            self.particles.remove(particle)

        self.time += self.rate

    def emit(self, position):
        if self.time > 1:
            if len(self.particles) < self.count:
                self.particles.append([-1, self.shape, self.getColor(0), position, 0, 0])
            self.time = 0

    def getColor(self, amount):
        r = abs(self.startColor[0] - self.endColor[0]) * amount + self.startColor[0]
        g = abs(self.startColor[1] - self.endColor[1]) * amount + self.startColor[1]
        b = abs(self.startColor[2] - self.endColor[2]) * amount + self.startColor[2]
        a = abs(self.startColor[3] - self.endColor[3]) * amount + self.startColor[3]
        return [max(r, self.endColor[0]), max(g, self.endColor[1]), max(b, self.endColor[2]), max(a, self.endColor[3])]