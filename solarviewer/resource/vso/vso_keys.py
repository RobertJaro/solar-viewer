import os
import pickle
import re

# parses entries from the txt-file and generates the keys used for VSO attributes
import solarviewer.resource.vso

resources_dir = os.path.dirname(solarviewer.resource.vso.__file__)
filepath = os.path.join(resources_dir, "VSO_keywords.txt")
store_file = os.path.join(resources_dir, "vso_key_value.pkl")


def parseEntries():
    data = open(filepath).readlines()
    dict = {}
    for line in data:
        pair = re.split(r'\t+', line.strip())

        key, value, desc = [None, None, None]
        if len(pair) == 2:
            key, value = pair
        elif len(pair) == 3:
            key, value, desc = pair
        else:
            continue

        if key not in dict:
            dict[key] = []
        dict[key].append((value, desc))

    file = open(store_file, "wb")
    pickle.dump(dict, file, pickle.HIGHEST_PROTOCOL)


def loadEntries():
    file = open(store_file, "rb")
    return pickle.load(file)


if __name__ == '__main__':
    parseEntries()
    print(loadEntries())
