import ply.yacc as yacc
import ply.lex as lex
import copy
from node import Node
from lexer import Lexer


class Grammar:
    def __init__(self, lexer, **kwargs):
        if lexer is None:
            raise Exception("Cannot procede without lexer rules")
        self.lexer = lexer.lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_statement(self, p):
        "statement : keyword arguments ';'"
        p[0] = Node("statement", [p[2]])

    def p_arguments(self, p):
        """arguments : arguments ',' expression
        | expression"""
        if len(p) == 2:
            p[0] = Node("arguments", [p[1]])
        else:
            p[0] = Node("arguments", p[1].children + [p[3]])

    def p_expression(self, p):
        """expression : expression '+' term
        | expression '*' term
        | term"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node("expression", [copy.deepcopy(p[1]), p[3], p[2]])

    def p_term(self, p):
        """term : number
        | string"""
        p[0] = Node("term", [p[1]])

    def p_error(self, p):
        if p:
            print(f"syntax error at '{p.value}'")
        else:
            print("syntax error at EOF")

    def build_ast(self, s):
        try:
            return self.parser.parse(s, lexer=self.lexer)
        except Exception as e:
            print(e)
