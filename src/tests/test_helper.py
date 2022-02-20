def load_shared_modules():
    import sys
    import os
    # adding Folder_2 to the system path
    sharedPath = os.path.join(os.getcwd(),'src', 'shared')
    sys.path.insert(1,sharedPath)
