import re

reserved_words = ['var', 'int', 'float', 'bool', 'string', 'while', 'bool', 'if', 'else', 'while', 'print', 'true', 'false']

pattern = re.compile(
    r'(?P<comment>//.*)|'
    r'(?P<string>"[^"]*")|'
    r'(?P<badString>"[^"]*)|' #para errores
    rf'(?P<reserved>\b(?:{"|".join(map(re.escape, reserved_words))})\b)|'
    r'(?P<id>[A-Za-z][A-Za-z0-9]*)|'
    r'(?P<badFloat>[0-9]*[\\.][0-9]+[\\.])|'
    r'(?P<float>[0-9]*[\\.][0-9]+)|'
    r'(?P<int>[0-9]+)|'
    r'(?P<opera>[+\-*/])|'
    r'(?P<operr>>=|<=|==|!=|>|<)|'
    r'(?P<symbol>=|;)|'
    r'(?P<operl>&&|\|\||!)|'
    r'(?P<lparen>\()|'
    r'(?P<rparen>\))|'
    r'(?P<lkey>\{)|'
    r'(?P<rkey>})|'
    r'(?P<lbracket>\[)|'
    r'(?P<rbracket>])|'
    r'(?P<whitespace>\s)|'
    r'(?P<unknown>.)'
)

#returns a list of tokens
def analisis_lexico(file_path):
    with open(file_path, 'r') as f:
        text = f.readlines()

    tokens = []
    line_counter = 0

    for line in text:
        line_counter += 1
        for match in pattern.finditer(line):
            for token, string in match.groupdict().items():
                if string is not None:
                    column = line.index(string) + 1 #BUG, index solo agarra el primer valor asi que x = x + 1 daria 2 columnas iguales
                    if token == "whitespace" or token == "comment":
                        pass
                    elif token == "unknown":
                        raise Exception(f'Unknown character. Line: {line_counter}, Column: {column}')
                    elif token == "badString":
                        raise  Exception(f'String not closed. Line: {line_counter}, Column: {column}')
                    elif token == "badFloat":
                        raise  Exception(f'Invalid Float number format. Line: {line_counter}, Column: {column}')
                    else:        
                        tokens.append((string, token, [line_counter, column]))
    tokens.append(("EOF", "EOF", []))
    return(tokens)

analisis_lexico("file.txt")