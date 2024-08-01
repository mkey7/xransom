import json

def openjson(file):
    '''
    opens a file and returns the json as a dict
    '''
    with open(file, encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data

def existingpost(post, posts):
    '''
    check if a post already exists in posts.json
    '''
    for p in posts:
        if p['ransom_name'].lower() == post["ransom_name"].lower() and post['title'] == p['title']:
            #dbglog('post already exists: ' + post_title)
            return True
    print('post does not exist: ' + post["title"])


