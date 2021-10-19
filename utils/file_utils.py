import json


def read_json(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    return data
