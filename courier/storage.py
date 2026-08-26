import json

def load_percels():
    with open("percels.json", "r") as file:
        percels = json.load(file)

        return percels