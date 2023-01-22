from mlconjug3 import constants
import tomlkit

def save_to_toml(file_path):
    data = {}
    for var in vars(constants):
        data[var] = vars(constants)[var]
    toml_str = tomlkit.dumps(data)
    with open(file_path, "w") as f:
        f.write(toml_str)

save_to_toml("constants.toml")
