from mlconjug3 import constants

import yaml

def save_to_yaml(file_path):
    data = {}
    for var in vars(constants):
        data[var] = vars(constants)[var]
    with open(file_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)

save_to_yaml("constants.yaml")
