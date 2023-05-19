import ply.yacc as pyacc
import ply.lex as plex


class Interpreter:
    states = (
        ("comment", "exclusive"),
        ("code", "exclusive"),
        #     ("string", "exclusive"),
        #     ("char", "exclusive"),
        #     ("numeric", "exclusive"),
        #     ("operator", "exclusive"),
        #     ("indentifier", "exclusive"),
        ("preprocessor", "exclusive"),
        ("macro", "exclusive"),
        #     ("keyword", "exclusive"),
    )

    @staticmethod
    @plex.TOKEN(r"INSERT")
    def t_COMMENT(t):
        """
        Transition to the 'inserting' state when in the INITIAL state.

        Args:
            t (Token): The token object.
        """

        t.lexer.begin("inserting")

    @staticmethod
    @plex.TOKEN(r"PRODUCT")
    def t_CODE(t):
        """
        Transition to the 'sell' state when in the INITIAL state.

        Args:
            t (Token): The token object.
        """

        t.lexer.begin("sell")

    @staticmethod
    @plex.TOKEN(r"REFILL")
    def t_PREPROCESS(t):
        """
        Transition to the 'refill' state when in the INITIAL state.

        Args:
            t (Token): The token object.
        """

        t.lexer.begin("refill")

    @staticmethod
    @plex.TOKEN(r"REFILL")
    def t_MACRO(t):
        """
        Transition to the 'refill' state when in the INITIAL state.

        Args:
            t (Token): The token object.
        """

        t.lexer.begin("refill")

    def __init__(self, **kwargs):
        """
        Initialize the Interpreter

        Attributes:
            lexer: An instance of the lexer created using the plex library.
        """

        self.lexer = plex.lex(module=self, **kwargs)
        import logging

        logging.basicConfig(
            level=logging.DEBUG,
            filename="parselog.txt",
            filemode="w",
            format="%(filename)10s:%(lineno)4d:%(message)s",
        )
        log = logging.getLogger()

        plex.lex(debug=True, debuglog=log)
        pyacc.yacc(debug=True, debuglog=log)


class Compiler:
    pass


def main():
    interpreter = Interpreter()


if __name__ == "__main__":
    main()
