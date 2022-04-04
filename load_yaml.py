import numpy as np
import yaml

from celestial_body_object import CelestialBodyObject
from simulation import CelestialBody


def load_objects(file_name):
    with open(file_name) as file:
        data = yaml.safe_load(file)
    body_objects = []
    for body_obj_data in data['objects']:
        body = CelestialBody(np.array(body_obj_data['pos'], dtype=float),
                             np.array(body_obj_data['v'], dtype=float),
                             body_obj_data['m'])
        body_obj = CelestialBodyObject(body,
                                       body_obj_data['name'],
                                       tuple(body_obj_data['color']),
                                       body_obj_data['size'])
        body_objects += [body_obj]
    return body_objects


def dump_objects(body_objects, file_name):
    yaml_out = {'objects': []}
    for body_obj in body_objects:
        yaml_out['objects'] += [{'pos': body_obj.body.pos.tolist(),
                                 'v': body_obj.body.v.tolist(),
                                 'm': body_obj.body.m,
                                 'name': body_obj.name,
                                 'color': list(body_obj.color),
                                 'size': body_obj.size}]
    with open(file_name, mode='w') as file:
        yaml.safe_dump(yaml_out, file)

