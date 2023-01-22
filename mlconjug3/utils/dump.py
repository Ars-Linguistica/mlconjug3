from mlconjug3 import constants

import yaml

def save_to_yaml(file_path):
    data = {}
    for var in vars(constants):
        if var.startswith("__"):
            continue
        try:
            print(f"trying to dump {var}")
            data[var] = vars(constants)[var]
        except:
            print(f"Error trying to dump {var}")
    with open(file_path, "w") as f:
        print(f"Writing file")
        yaml.dump(data, f, default_flow_style=False)

save_to_yaml("constants.yaml")
