import json

def load_json_config(file_path):
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
    return json_data
