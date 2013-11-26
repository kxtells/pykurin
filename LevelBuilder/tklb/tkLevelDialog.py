#
#
# Dialog to handle Level related information such as name, start and end position,
# base pykurin path etc.
#
#

import tkMessageBox

class tkLevelDialog(Frame):
    def __init__(self, master = None, datacontainer = None):
        assert datacontainer != None


