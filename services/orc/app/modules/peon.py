import sys
import json
import os
import random

sys.path.insert(0,'/app')

dictionary = json.load(open(os.path.join(os.environ.get("PEON_INSTALL_PATH", "/app"), "dictionary.json"), 'r'))

def get_warcamp_name():
    prefix = dictionary['server_names']['prefix']
    suffix = dictionary['server_names']['suffix']
    return (random.choice(prefix) + random.choice(suffix))

if __name__ == "__main__":
    print(get_warcamp_name())