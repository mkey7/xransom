import json

def openjson(file):
    '''
    opens a file and returns the json as a dict
    '''
    with open(file, encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data


