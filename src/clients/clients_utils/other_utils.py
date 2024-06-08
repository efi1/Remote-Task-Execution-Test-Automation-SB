from importlib.resources import files
from pathlib import Path
from src.cfg.cfg_global import settings
import json


class Obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)


def dict_to_obj(d: dict) -> Obj:
    """
    Convert a dict to an object type
    :param d: a dict object
    :return: an object with the dict content
    """
    return json.loads(json.dumps(d), object_pairs_hook=Obj)

