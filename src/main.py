import lexer
import parser
import ast

file_path = "file.txt"

parser.tokens = lexer.analisis_lexico(file_path)
#tokens -> [string, tokentype, [line, column]]
tree = parser.program()
tree.print_tree()