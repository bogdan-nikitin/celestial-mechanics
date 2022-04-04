from dataclasses import dataclass
import numpy.typing as npt
import numpy as np


G = 6.67e-11


@dataclass
class CelestialBody:
    pos: npt.NDArray[float]
    v: npt.NDArray[float]
    m: float
    # ak1: npt.NDArray[float] = np.array([0, 0], dtype=float)
    # ak2: npt.NDArray[float] = np.array([0, 0], dtype=float)
    # ak3: npt.NDArray[float] = np.array([0, 0], dtype=float)


def magnitude(vec):
    return np.sqrt(vec.dot(vec))


def get_a(body1, body2, delta_pos=np.array([0, 0], dtype=float)):
    r12 = body2.pos - body1.pos - delta_pos
    r = magnitude(r12)
    f1 = G * body1.m * body2.m / r ** 2 * r12 / r
    a1 = f1 / body1.m
    return a1


def do_iteration(bodies, time=1):
    # for body in bodies:
    #     body.pos += body.v * time * 0.5
    for body1 in bodies:
        for body2 in bodies:
            if body1 is not body2:
                r12 = body2.pos - body1.pos
                r = magnitude(r12)
                # f1 = G * body1.m * body2.m / r ** 2 * r12 / r
                # a1 = f1 / body1.m
                a1 = G * body2.m / r ** 3 * r12
                body1.v += a1 * time

                # body1.ak1 = ak1 = get_a(body1, body2)
                # body1.ak2 = ak2 = get_a(body1, body2, time / 2 * ak1)
                # body1.ak3 = ak3 = get_a(body1, body2, time / 2 * ak2)
                # ak4 = get_a(body1, body2, time * ak3)
                # body1.v += time / 6 * (ak1 + 2 * ak2 + 2 * ak3 + ak4)
    for body in bodies:
        # vk1 = body.v
        # vk2 = body.v + time / 2 * body.ak1
        # vk3 = body.v + time / 2 * body.ak2
        # vk4 = body.v + time * body.ak3
        # body.pos += time / 6 * (vk1 + 2 * vk2 + 2 * vk3 + vk4)

        body.pos += body.v * time


def get_energy(bodies):
    e = 0
    for body1 in bodies:
        e += body1.m * magnitude(body1.v) ** 2 / 2
        for body2 in bodies:
            if body1 is not body2:
                e -= G * body1.m * body2.m / magnitude(body1.pos - body2.pos)
    return e
