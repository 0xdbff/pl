import ply.yacc as yacc
import ply.lex as lex
from node import Node
from lexer import Lexer


class Grammar:
    def __init__(self, lexer, **kwargs):
        if lexer is None:
            raise Exception("Cannot proceed without lexer rules")
        self.lexer = lexer.lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    precedence = (
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("right", "UMINUS"),
    )

    names = {}

    def p_statement_assign(self, p):
        'statement : NAME "=" expression'
        self.names[p[1]] = p[3]
        p[0] = Node("assign", value=p[1], children=[p[3]])

    def p_statement_expr(self, p):
        "statement : expression"
        p[0] = Node("statement", children=[p[1]])

    def p_expression_binop(self, p):
        """expression : expression '+' expression
        | expression '-' expression
        | expression '*' expression
        | expression '/' expression"""
        p[0] = Node("binop", value=p[2], children=[p[1], p[3]])

    def p_expression_uminus(self, p):
        "expression : '-' expression %prec UMINUS"
        p[0] = Node("uminus", children=[p[2]])

    def p_expression_group(self, p):
        "expression : '(' expression ')'"
        p[0] = Node("group", children=[p[2]])

    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = Node("number", value=p[1])

    def p_expression_name(self, p):
        "expression : NAME"
        p[0] = Node("name", value=p[1])

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    def build_ast(self, s):
        try:
            return self.parser.parse(s + "\n", tracking=True, lexer=self.lexer)
        except Exception as e:
            print(e)
