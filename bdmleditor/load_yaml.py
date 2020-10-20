import yaml


def load_yamlinfo(filename):
    with open(filename, 'r') as yml:
        config = yaml.safe_load(yml)
    return config


def return_token(yaml_info):
    return yaml_info['token']


def load_userID(yaml_info, user_name):
    for user_ids in yaml_info['user_info']:
        if user_ids.get(user_name) is not None:
            return user_ids.get(user_name)
    return
