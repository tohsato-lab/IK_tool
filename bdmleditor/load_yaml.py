import yaml


def load_yamlinfo(filename):
    with open(filename, 'r') as yml:
        config = yaml.safe_load(yml)
        print(config['data_range'])
    return config['data_range']
