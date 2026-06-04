import main

def read(terminal, estado):
    if len(main.tokens) == 0:
        return False
    if estado:
        if main.tokens[0][0] == terminal:
            main.tokens.pop(0)
            return True
        return False
    else:
        if main.tokens[0][1] == terminal:
            main.tokens.pop(0)
            return True
        return False

def program():
    if not item_list(): raise Exception
    
    if not read("EOF", True):
        raise Exception("Expected EOF")
    
    return True

def item_list():
    while item():
        pass
    return True

def item():
    if decl(): return True
    elif stmt(): return True
    return False

def decl():
    if read("var", True):
        if type():
            if read("id", False):
                if read(";", True):
                    return True
    return False 

def type():
    if read("int",True): return True
    elif read("float", True): return True
    elif read("bool", True): return True
    elif read("string", True): return True
    return False

def stmt():
    if assign():
        if read(";", True): return True
    elif print_stmt():
        if read(";", True): return True
    elif if_stmt(): return True
    elif while_stmt(): return True
    elif block(): return True
    return False

def block():
    if read("{", True):
        if item_list():
            if read("}", True):
                return True
    return False

def assign():
    if read("id", False):
        if read("=", True):
            if expr():
                return True
    return False

def print_stmt():
    if read("print", True):
        if read("(", True):
            if expr():
                if read(")", True):
                    return True
    return False

def if_stmt():
    if read("if", True):
        if read("(", True):
            if expr():
                if read(")", True):
                    if block():
                        if else_part():
                            return True
    return False

def else_part():
    if read("else", True):
        if not block(): raise Exception
    return True
    

def while_stmt():
    if read("while", True):
        if read("(", True):
            if expr():
                if read(")", True):
                    if block():
                        return True
    return False

def expr():
    if not logic_or(): raise Exception
    return True

def logic_or():
    if logic_and():
        logic_or_loop()
        return True
    return False

def logic_or_loop():
    if read("||", True):
        if logic_and():
            if logic_or_loop():
                return True
            return True
        raise Exception #no estoy 100% seguro si aqui es raise Exception o False pero creo que es Exception pq no hay otra posibilidad
    return True

def logic_and():
    if equality():
        logic_and_loop()
        return True
    return False

def logic_and_loop():
    if read("&&", True):
        if equality():
            if logic_and_loop():
                return True
            return True
        raise Exception #no estoy 100% seguro si aqui es raise Exception o False pero creo que es Exception pq no hay otra posibilidad
    return True

def equality():
    if relation():
        if read("==", True) or read("!=", True):
            if not relation():
                raise Exception
            return True
        return True
    return False

def relation():
    if term():
        if read("<", True) or read("<=", True) or read(">", True) or read(">=", True):
            if not term():
                raise Exception
            return True
        return True
    return False

def term():
    if factor():
        term_loop()
        return True
    return False

def term_loop():
    if read("+", True) or read("-", True):
        if factor():
            if term_loop():
                return True
            return True
        raise Exception #no estoy 100% seguro si aqui es raise Exception o False pero creo que es Exception pq no hay otra posibilidad
    return True

def factor():
    if unary():
        if factor_loop():
            return True
        return True
    return False

def factor_loop():
    if read("*", True) or read("/", True):
        if unary():
            if factor_loop():
                return True
            return True
        raise Exception #no estoy 100% seguro si aqui es raise Exception o False pero creo que es Exception pq no hay otra posibilidad
    return True

def unary():
    if read("!", True) or read("-", True):
        if unary():
            return True
        return False
    elif primary():
        return True
    return False

def primary():
    if read("int", False) or read("float", False) or read("string", False) or read("true", True) or read("false", True) or read("id", False):
        return True 
    if read("(", True):
        if expr():
            if read(")", True):
                return True
            return False
        return False
    return False
