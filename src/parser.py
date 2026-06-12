import ast

tokens = []

def consume(terminal, state):
    if len(tokens) == 0:
        return False
    if state:
        if tokens[0][0] == terminal:
            tok = tokens.pop(0)
            return ast.Node(category=tok[1], value=tok[0], line=tok[2])
        return False
    else:
        if tokens[0][1] == terminal:
            tok = tokens.pop(0)
            return ast.Node(category=tok[1], value=tok[0], line=tok[2])
        return False

def peek_literal():
    if len(tokens) == 0:
        return None
    return tokens[0][0]

def peek_type():
    if len(tokens) == 0:
        return None
    return tokens[0][1]


def program():
    node = ast.Node("program")

    items = item_list()
    if items:
        node.add_child(items)

    eof = consume("EOF", True)
    if not eof:
        raise Exception("Expected EOF")
    node.add_child(eof)

    return node

def item_list():
    node = ast.Node("item_list")
    while True:
        i = item()
        if not i:
            break
        node.add_child(i)
    return node

def item():
    if peek_literal() == "var":
        return decl()
    return stmt()

def decl():
    node = ast.Node("decl")
    kw = consume("var", True)
    if kw:
        node.add_child(kw)
        t = type()
        if t:
            node.add_child(t)
            id_node = consume("id", False)
            if id_node:
                node.add_child(id_node)
                semi = consume(";", True)
                if semi:
                    node.add_child(semi)
                    return node
    return False

def type():
    node = (
        consume("int", True) or
        consume("float", True) or
        consume("bool", True) or
        consume("string", True)
    )
    return node

def stmt():
    if peek_type() == "id":
        node = ast.Node("stmt")
        a = assign()
        if a:
            node.add_child(a)
            semi = consume(";", True)
            if semi:
                node.add_child(semi)
                return node
    elif peek_literal() == "print":
        node = ast.Node("stmt")
        p = print_stmt()
        if p:
            node.add_child(p)
            semi = consume(";", True)
            if semi:
                node.add_child(semi)
                return node
    elif peek_literal() == "if":
        return if_stmt()
    elif peek_literal() == "while":
        return while_stmt()
    elif peek_literal() == "{":
        return block()
    return False

def block():
    node = ast.Node("block")
    lb = consume("{", True)
    if lb:
        node.add_child(lb)
        items = item_list()
        if items:
            node.add_child(items)
        rb = consume("}", True)
        if rb:
            node.add_child(rb)
            return node
    return False

def assign():
    node = ast.Node("assign")
    id_node = consume("id", False)
    if id_node:
        node.add_child(id_node)
        eq = consume("=", True)
        if eq:
            node.add_child(eq)
            e = expr()
            if e:
                node.add_child(e)
                return node
    return False

def print_stmt():
    node = ast.Node("print")
    kw = consume("print", True)
    if kw:
        node.add_child(kw)
        lp = consume("(", True)
        if lp:
            node.add_child(lp)
            e = expr()
            if e:
                node.add_child(e)
                rp = consume(")", True)
                if rp:
                    node.add_child(rp)
                    return node
    return False

def if_stmt():
    node = ast.Node("if")
    kw = consume("if", True)
    if kw:
        node.add_child(kw)
        lp = consume("(", True)
        if lp:
            node.add_child(lp)
            e = expr()
            if e:
                node.add_child(e)
                rp = consume(")", True)
                if rp:
                    node.add_child(rp)
                    b = block()
                    if b:
                        node.add_child(b)
                        ep = else_part()
                        if ep:
                            node.add_child(ep)
                        return node
    return False

def else_part():
    node = ast.Node("else")
    kw = consume("else", True)
    if kw:
        node.add_child(kw)
        b = block()
        if b:
            node.add_child(b)
            return node
        raise Exception("Expected block after else")
    return None  # else es opcional

def while_stmt():
    node = ast.Node("while")
    kw = consume("while", True)
    if kw:
        node.add_child(kw)
        lp = consume("(", True)
        if lp:
            node.add_child(lp)
            e = expr()
            if e:
                node.add_child(e)
                rp = consume(")", True)
                if rp:
                    node.add_child(rp)
                    b = block()
                    if b:
                        node.add_child(b)
                        return node
    return False

def expr():
    node = ast.Node("expr")
    lo = logic_or()
    if not lo:
        raise Exception("Expected expression")
    node.add_child(lo)
    return node

def logic_or():
    node = ast.Node("logic_or")
    la = logic_and()
    if la:
        node.add_child(la)
        logic_or_loop(node)
        return node
    return False

def logic_or_loop(parent):
    op = consume("||", True)
    if op:
        parent.add_child(op)
        la = logic_and()
        if la:
            parent.add_child(la)
            logic_or_loop(parent)
            return True
        raise Exception("Expected operand after '||'")
    return True

def logic_and():
    node = ast.Node("logic_and")
    eq = equality()
    if eq:
        node.add_child(eq)
        logic_and_loop(node)
        return node
    return False

def logic_and_loop(parent):
    op = consume("&&", True)
    if op:
        parent.add_child(op)
        eq = equality()
        if eq:
            parent.add_child(eq)
            logic_and_loop(parent)
            return True
        raise Exception("Expected operand after '&&'")
    return True

def equality():
    node = ast.Node("equality")
    r = relation()
    if r:
        node.add_child(r)
        op = consume("==", True) or consume("!=", True)
        if op:
            node.add_child(op)
            r2 = relation()
            if not r2:
                raise Exception("Expected operand after equality operator")
            node.add_child(r2)
        return node
    return False

def relation():
    node = ast.Node("relation")
    t = term()
    if t:
        node.add_child(t)
        op = (
            consume("<=", True) or consume(">=", True) or
            consume("<", True) or consume(">", True)
        )
        if op:
            node.add_child(op)
            t2 = term()
            if not t2:
                raise Exception("Expected operand after relational operator")
            node.add_child(t2)
        return node
    return False

def term():
    node = ast.Node("term")
    f = factor()
    if f:
        node.add_child(f)
        term_loop(node)
        return node
    return False

def term_loop(parent):
    op = consume("+", True) or consume("-", True)
    if op:
        parent.add_child(op)
        f = factor()
        if f:
            parent.add_child(f)
            term_loop(parent)
            return True
        raise Exception("Expected operand after '+' or '-'")
    return True

def factor():
    node = ast.Node("factor")
    u = unary()
    if u:
        node.add_child(u)
        factor_loop(node)
        return node
    return False

def factor_loop(parent):
    op = consume("*", True) or consume("/", True)
    if op:
        parent.add_child(op)
        u = unary()
        if u:
            parent.add_child(u)
            factor_loop(parent)
            return True
        raise Exception("Expected operand after '*' or '/'")
    return True

def unary():
    node = ast.Node("unary")
    op = consume("!", True) or consume("-", True)
    if op:
        node.add_child(op)
        u = unary()
        if u:
            node.add_child(u)
            return node
        return False
    p = primary()
    if p:
        node.add_child(p)
        return node
    return False

def primary():
    node = ast.Node("primary")
    lit = (
        consume("int", False) or
        consume("float", False) or
        consume("string", False) or
        consume("true", True) or
        consume("false", True) or
        consume("id", False)
    )
    if lit:
        node.add_child(lit)
        return node
    lp = consume("(", True)
    if lp:
        node.add_child(lp)
        e = expr()
        if e:
            node.add_child(e)
            rp = consume(")", True)
            if rp:
                node.add_child(rp)
                return node
        return False
    return False