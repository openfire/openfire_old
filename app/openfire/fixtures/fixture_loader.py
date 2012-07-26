import fixture_util as util
import json
import os


# Model indexes.
FIXTURE_INDEXES = ['user', 'update', 'project', 'category', 'activity']


'''
    List all fixture json files here, without the '.json' extension.

    Each item in this array is a tuple with the following values,
    which represents a single object type and util function:
        - JSON file name, without the .json extension.
        - Util function used to save the object type.
        - A unique field used for key relationships.

    Order of these fixtures matter.
'''
FIXTURE_FILES = [
    # ( <json file>, <function used to save the object>, <unique field used for key relations> )
    ('user', util.create_user, 'username'),
    ('contribution_type', util.create_contribution_type, 'slug'),
    ('category', util.create_category, 'slug'),
    ('proposal', util.create_proposal, 'name'),
    ('project', util.create_project, 'name'),
    ('goal', util.create_goal, 'parent_key'),
    ('tier', util.create_tier, 'name'),
    ('avatar', util.create_avatar, 'name'),
    ('video', util.create_video, 'name'),
    ('custom_url', util.create_custom_url, 'slug'),
]

def make_fixture_key(val, data):

    ''' Used to fix keys. Gets a value from the data dict. '''

    ret = data
    for getter in val.split('__'):
        ret = ret.get(getter)
    return ret

def fix_fixture_keys(obj, data):

    '''
    Replaces all the key fields with the appropriate keys.

    Each field ending in '_key' or '_keys' will contain a series
    of data dictionary keys separated by two underscores. Those fields
    are replaced using make_fixture_key.
    '''

    for key, val in obj.items():
        if key[-4:] == '_key':
            obj[key] = make_fixture_key(val, data)
        if key[-5:] == '_keys':
            keys = []
            for key_val in val:
                keys.append(make_fixture_key(key_val, data))
            obj[key] = keys
    return obj

def load_fixtures():

    '''
    Used to load all the fixtures from the fixtures lists above.

    Go through each of the fixtures listed and create each object in the fixture.
    '''

    util.build_indexes(FIXTURE_INDEXES)

    loaded_data = {}
    for name, create_func, unique_slug in FIXTURE_FILES:
        filename = os.path.join(os.path.dirname(__file__), 'json', name + '.json')
        with open(filename) as fixture:
            fixture_data = json.loads(fixture.read())

        loaded_data[name] = {}
        for i in range(len(fixture_data)):
            obj_data = fixture_data[i]
            obj_data = fix_fixture_keys(obj_data, loaded_data)
            loaded_data[name][obj_data[unique_slug]] = create_func(**obj_data)
