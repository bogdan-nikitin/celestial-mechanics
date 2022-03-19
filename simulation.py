from dataclasses import dataclass
import numpy.typing as npt
import numpy as np


G = 6.67e-11


@dataclass
class CelestialBody:
    pos: npt.NDArray[float]
    v: npt.NDArray[float]
    m: float


def magnitude(vec):
    return np.sqrt(vec.dot(vec))


def do_iteration(bodies, time=1):
    # for body in bodies:
    #     body.pos += body.v * time * 0.5
    for body1 in bodies:
        for body2 in bodies:
            if body1 is not body2:
                r12 = body2.pos - body1.pos
                r = magnitude(r12)
                f1 = G * body1.m * body2.m / r ** 2 * r12 / r
                a1 = f1 / body1.m
                body1.v += a1 * time
                # body1.v +=
    for body in bodies:
        body.pos += body.v * time


