
import json

def is_none_or_empty_str(str):

    if str == None or len(str) == 0:
        return True

    return False

def is_int(num):

    if isinstance(num, int):
        return True

    return False

def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)

def load_shared_modules():
    import sys
    import os
    # adding Folder_2 to the system path
    sharedPath = os.path.join(os.getcwd(),'src', 'shared')
    sys.path.insert(1,sharedPath)