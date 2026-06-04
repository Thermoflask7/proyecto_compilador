import main

def read(terminal, estado):
    if estado:
        if main.tokens[0][0] == terminal:
            main.tokens.pop(0)
            return True
        else: return False
    else:
        if main.tokens[0][1] == terminal:
            main.tokens.pop(0)
            return True
        else: return False

def program():
    if not item_list(): raise Exception
    #end of file

def item_list():
    if item():
        if not item_list(): raise Exception
        return True
    else: return True

def item():
    if decl(): return True
    elif stmt(): return True
    else: return False

def decl():
    if read("var", True):
        if type():
            if read("id", False):
                if read(";", True):
                    return True
    return False 

def type():
    pass

def stmt():
    pass

def block():
    pass

def assign():
    pass

def print():
    pass

def if_stmt():
    pass

def else_part():
    pass

def while_stmt():
    pass

def expr():
    if not logic_or(): raise Exception

def logic_or():
    pass

def logic_and():
    pass

def equality():
    pass

def relation():
    pass

def term():
    pass

def factor():
    pass

def unary():
    pass

def primary():
    pass
