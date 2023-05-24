import ply.yacc as yacc
from node import Node


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

    vars = {}

    def p_statement_print(self, p):
        """statement : PRINT arguments"""
        p[0] = Node("print", children=[p[2]])

    def p_statemnet_setvar(self, p):
        """statement : var_declaration"""
        p[0] = Node("set_var", children=[p[1]])

    def p_arguments_expression(self, p):
        """arguments : arguments ',' expression
        | expression"""
        if len(p) > 2:
            p[0] = Node(
                "arguments",
                children=[*p[1].children, Node("expression", children=[p[3]])],
            )
        else:
            p[0] = Node("arguments", children=[Node("expression", children=[p[1]])])

    # def p_statement_var(self, p):
    #     """statement : VAR NAME "=" expression
    #     | VAR NAME
    #     | """
    #     self.vars[p[2]] = p[4]
    #     p[0] = Node("var", value=p[2], children=[p[4]])

    def p_statement_var(self, p):
        """statement : VAR var_declaration_list"""
        p[0] = Node("var", children=[p[2]])

    def p_var_declaration_list(self, p):
        """var_declaration_list : var_declaration_list ',' var_declaration
        | var_declaration"""
        if len(p) > 2:
            p[0] = Node("var_declaration_list", children=[*p[1].children, p[3]])
        else:
            p[0] = Node("var_declaration_list", children=[p[1]])

    def p_var_declaration(self, p):
        """var_declaration : NAME '=' expression
        | NAME"""
        if len(p) > 2:
            p[0] = Node("var_declaration", value=p[1], children=[p[3]])
        else:
            p[0] = Node("var_declaration", value=p[1])

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

    def p_expression_string(self, p):
        "expression : STRING"
        p[0] = Node("string", value=p[1])

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    def build_ast(self, s):
        try:
            return self.parser.parse(s, tracking=True, lexer=self.lexer)
        except Exception as e:
            print(e)
