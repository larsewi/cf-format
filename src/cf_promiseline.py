from cf_classguard import CFClassGuard
from cf_comment import CFComment
from cf_syntax import CFSyntax
from cf_quotedstring import CFQuotedString
from cf_constraint import CFConstraint
from token import TokenKind


class CFPromiseLine(CFSyntax):
    def __init__(self, debug):
        super().__init__("promiseline", debug)

    @staticmethod
    def parse(tokens, debug):
        promiseline = CFPromiseLine(debug)
        promiseline.enter_parser()
        nonterms = promiseline._nonterms

        # Parse classguard if any
        if tokens.current().kind() is TokenKind.CLASS_GUARD:
            classguard = CFClassGuard.parse(tokens, debug)
            assert classguard is not None
            nonterms.append(classguard)

        # Parse comments if any
        while tokens.current().kind() is TokenKind.COMMENT:
            comment = CFComment.parse(tokens, debug)
            assert comment is not None
            nonterms.append(classguard)

        # Parse promiser
        current = tokens.current()
        if current.kind() is not TokenKind.QUOTED_STRING:
            promiseline.parser_error(current, TokenKind.QUOTED_STRING)
        promiser = CFQuotedString.parse(tokens, debug)
        assert promiser is not None
        nonterms.append(promiser)

        # Parse promisee
        current = tokens.current()
        if current.kind() is TokenKind.THIN_ARROW:
            # TODO: Implement promisee, what ever that is ?
            pass

        # Parse constraints
        current = tokens.current()
        while current.kind() is not TokenKind.SEMICOLON:
            constraint = CFConstraint.parse(tokens, debug)
            nonterms.append(constraint)

            current = tokens.current()
            if current.kind() is TokenKind.COMMA:
                tokens.skip(TokenKind.COMMA)
                current = tokens.current()
            else:
                break

        if current.kind() is not TokenKind.SEMICOLON:
            promiseline.parser_error(current, TokenKind.COMMA, TokenKind.SEMICOLON)
        tokens.skip(TokenKind.SEMICOLON)

        promiseline.leave_parser()
        return promiseline

    def pretty_print(self, cursor=0):
        nonterms = self._nonterms
        buf = ""

        # classguard
        nonterm = nonterms.pop(0)
        if isinstance(nonterm, CFClassGuard):
            buf += nonterm.pretty_print() + "\n"
            nonterm = nonterms.pop(0)

        # comment
        while isinstance(nonterm, CFComment):
            buf += "  " + nonterm.pretty_print() + "\n"
            nonterm = nonterms.pop(0)

        # promiser
        print(type(nonterm).__name__)
        assert isinstance(nonterm, CFQuotedString)
        buf += "    " + nonterm.pretty_print()
        nonterm = nonterms.pop(0)

        return ""
