"""
This super class is inherited by other objects in the game

Create an object from a json file by passing the filename into init

Ex. x = MansionObject("../resources/player/player.json")
"""

import json


class MansionObject:

    def __init__(self, file_name):
        self.__dict__ = self.get_json(file_name)

    def get_json(self, file_name):
        with open(file_name, "r") as read_file:
            res = json.load(read_file, object_hook=self._decode_dict)
        return res

    def save_json(self, file_name):
        with open(file_name, "w+") as write_file:
            json.dump(self.__dict__, write_file)

    def _decode_list(self, data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = self._decode_list(item)
            elif isinstance(item, dict):
                item = self._decode_dict(item)
            rv.append(item)
        return rv

    def _decode_dict(self, data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self._decode_list(value)
            elif isinstance(value, dict):
                value = self._decode_dict(value)
            rv[key] = value
        return rv