import lexer
import parser

file_path = 'file.txt'

tokens = lexer.analisis_lexico(file_path)
#tokens -> [string, tokentype, [line, column]]