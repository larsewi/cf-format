from os import write
from cf_comment import CFComment
from cf_identifier import CFIdentifier
from cf_syntax import CFSyntax
from token import TokenKind


class CFArgList(CFSyntax):
    def __init__(self, debug):
        super().__init__("arglist", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        arglist = CFArgList(debug)
        arglist.enter_parser()

        tokens.skip(TokenKind.LEFT_PAR)

        while True:
            CFComment.parse_while(arglist, tokens, debug)

            current = tokens.current()
            if current.kind() is not TokenKind.IDENTIFIER:
                arglist.parser_error(current, TokenKind.IDENTIFIER)
            identifier = CFIdentifier.parse(tokens, debug)
            assert identifier is not None
            arglist._nonterms.append(identifier)

            CFComment.parse_while(arglist, tokens, debug)
            current = tokens.current()
            if current.kind() is TokenKind.COMMA:
                tokens.skip(TokenKind.COMMA)
            else:
                break

        current = tokens.current()
        if current.kind() is not TokenKind.RIGHT_PAR:
            arglist.parser_error(current, TokenKind.RIGHT_PAR, TokenKind.COMMA)
        tokens.skip(TokenKind.RIGHT_PAR)

        arglist.leave_parser()
        return arglist

    def pretty_print(self, cursor=0):
        nonterms = self._nonterms

        # Wrap if there are comments in arglist
        should_wrap = any(isinstance(el, CFComment) for el in nonterms)

        if not should_wrap:
            buf = "(" + ", ".join(map(lambda el: el.pretty_print(), nonterms)) + ")"
            if cursor + len(buf) <= self._WRAP_LENGTH:
                return buf

        count = len(list(filter(lambda el: isinstance(el, CFIdentifier), nonterms)))
        buf = ""
        last_was_identifier = False
        for nonterm in nonterms:
            if isinstance(nonterm, CFComment):
                if last_was_identifier:
                    buf += " " + nonterm.pretty_print()
                else:
                    buf += "\n  " + " " * cursor + nonterm.pretty_print()
                last_was_identifier = False
            else:
                assert isinstance(nonterm, CFIdentifier)
                buf += "\n  " + " " * cursor + nonterm.pretty_print()
                if count > 1:
                    buf += ","
                    count -= 1
                last_was_identifier = True

        return "(" + buf + "\n" + " " * cursor + ")"
