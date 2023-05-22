# arith_grammar.py
from arith_lexer import ArithLexer
import ply.yacc as pyacc


class ArithGrammar:
    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None

    def build(self, **kwargs):
        self.lexer = ArithLexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)

    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)

    # gramática..
    def p_expr(self, p):
        """E : E '+' T
          | T
        T : T '*' F
          | F
        F : '(' E ')'
          | num"""
        # p[0] = p[1]
        p[0] = "sucesso!"

    def p_error(self, p):
        if p:
            print(f"Syntax error: unexpected '{p.type}'")
        else:
            print("Syntax error: unexpected end of file")
        exit(1)
