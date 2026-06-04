import main

def consume(terminal, estado):
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

def peek_literal():
    if len(main.tokens) == 0:
        return None
    return main.tokens[0][0]

def peek_type():
    if len(main.tokens) == 0:
        return None
    return main.tokens[0][1]



def program():
    if not item_list(): raise Exception
    
    if not consume("EOF", True):
        raise Exception("Expected EOF")
    
    return True

def item_list():
    while item():
        pass
    return True

def item():
    if peek_literal() == "var":
        return decl()
    
    return stmt()

def decl():
    if consume("var", True):
        if type():
            if consume("id", False):
                if consume(";", True):
                    return True
    return False 

def type():
    if consume("int",True): return True
    elif consume("float", True): return True
    elif consume("bool", True): return True
    elif consume("string", True): return True
    return False

def stmt():
    if peek_type() == "id":
        if assign():
            return consume(";", True)
    elif peek_literal() == "print":
        if print_stmt():
            return consume(";", True)
    elif peek_literal() == "if":
            return if_stmt()
    elif peek_literal() == "while":
        return while_stmt()
    elif peek_literal() == "{":
        return block()
    return False

def block():
    if consume("{", True):
        if item_list():
            if consume("}", True):
                return True
    return False

def assign():
    if consume("id", False):
        if consume("=", True):
            if expr():
                return True
    return False

def print_stmt():
    if consume("print", True):
        if consume("(", True):
            if expr():
                if consume(")", True):
                    return True
    return False

def if_stmt():
    if consume("if", True):
        if consume("(", True):
            if expr():
                if consume(")", True):
                    if block():
                        if else_part():
                            return True
    return False

def else_part():
    if consume("else", True):
        if not block(): raise Exception
    return True
    

def while_stmt():
    if consume("while", True):
        if consume("(", True):
            if expr():
                if consume(")", True):
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
    if consume("||", True):
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
    if consume("&&", True):
        if equality():
            if logic_and_loop():
                return True
            return True
        raise Exception #no estoy 100% seguro si aqui es raise Exception o False pero creo que es Exception pq no hay otra posibilidad
    return True

def equality():
    if relation():
        if consume("==", True) or consume("!=", True):
            if not relation():
                raise Exception
            return True
        return True
    return False

def relation():
    if term():
        if consume("<", True) or consume("<=", True) or consume(">", True) or consume(">=", True):
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
    if consume("+", True) or consume("-", True):
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
    if consume("*", True) or consume("/", True):
        if unary():
            if factor_loop():
                return True
            return True
        raise Exception #no estoy 100% seguro si aqui es raise Exception o False pero creo que es Exception pq no hay otra posibilidad
    return True

def unary():
    if consume("!", True) or consume("-", True):
        if unary():
            return True
        return False
    elif primary():
        return True
    return False

def primary():
    if consume("int", False) or consume("float", False) or consume("string", False) or consume("true", True) or consume("false", True) or consume("id", False):
        return True 
    if consume("(", True):
        if expr():
            if consume(")", True):
                return True
            return False
        return False
    return False
