def read(tokens):
    pass

def program():
    if not item_list(): raise Exception
    #end of file

def item_list():
    if item():
        if not item_list(): raise Exception
        return True
    else: return True

def item():
    pass
