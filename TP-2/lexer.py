import ply.lex as lex
from reserved import reserved as py_c_keywords


class Lexer:
    reserved = py_c_keywords

    keywords = {
        "stdout": "stdout",
        "var": "var",
        "const": "const",
        "stdin": "stdin",
        "fn": "fn",
        "return": "return",
        "while": "while",
        "for": "for",
        "in": "in",
        "not": "not",
        "and": "and",
        "or": "or",
        "break": "break",
        "continue": "continue",
    }

    tokens = [
        "string",
        "number",
        # "comma",
        # "semicolon",
        # "times",
        # "plus",
        "identifier",
        "keyword",
    ]  # + list(keywords.values())

    literals = ["{", "}", "+", "-", "*", "/", ">", "<", "&", "|", ";", ","]
    t_ignore = " \t"

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    @lex.TOKEN(r"[a-zA-Z_][a-zA-Z_0-9]*")
    def t_identifier(self, t):
        try:
            if self.keywords.get(t.value) is not None:
                t.type = "keyword"
            elif self.reserved.get(t.value) is not None:
                t.type = "identifier"
            else:
                raise ValueError(
                    "The token is not a valid identifier or keyword, "
                    "check the list of reserved keywords!"
                )
            return t
        except ValueError as e:
            print(e)

    @lex.TOKEN(r'"[^"]*"')
    def t_string(self, t):
        try:
            t.value = t.value[1:-1]
            return t
        except ValueError as e:
            print(e)

    @lex.TOKEN(
        r"-?0[bB][01]+|-?0[oO][0-7]+|-?0[xX][0-9a-fA-F]+|-?\d+(\.\d+)?(e[-+]?\d+)?"
    )
    def t_number(self, t):
        try:
            if "e" in t.value or "." in t.value:
                t.value = float(t.value)
            elif t.value.lower().startswith("0b"):
                t.value = int(t.value, 2)
            elif t.value.lower().startswith("0o"):
                t.value = int(t.value, 8)
            elif t.value.lower().startswith("0x"):
                t.value = int(t.value, 16)
            else:
                t.value = int(t.value)
        except ValueError:
            print(f"Could not parse number: {t.value}")
        return t

    @staticmethod
    @lex.TOKEN(r"//.*")
    def t_comment(t):
        return

    @staticmethod
    @lex.TOKEN(r"/\*(.|\n)*?\*/")
    def t_multiline_comment(t):
        return

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
