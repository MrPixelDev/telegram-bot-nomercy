import json


def read_json(path: str):
    with open(path) as file:
        data = json.load(file)
        return data


def write_json(path: str, data: dict):
    with open(path, 'w') as file:
        json.dump(data, file)
