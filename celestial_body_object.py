from dataclasses import dataclass
from typing import List

from simulation import CelestialBody


@dataclass
class CelestialBodyTrajectory:
    x: List[float]
    y: List[float]


@dataclass
class CelestialBodyObject:
    def __post_init__(self):
        self.trajectory = CelestialBodyTrajectory(
            [self.body.pos[0]], [self.body.pos[1]]
        )

    body: CelestialBody
    name: str
    color: (int, int, int)
    size: float
    trajectory: CelestialBodyTrajectory = None


def update_trajectories(body_objects):
    for body_obj in body_objects:
        body_obj.trajectory.x += [body_obj.body.pos[0]]
        body_obj.trajectory.y += [body_obj.body.pos[1]]