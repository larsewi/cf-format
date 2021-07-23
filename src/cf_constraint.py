from cf_identifier import CFIdentifier
from cf_syntax import CFSyntax
from token import Token, TokenKind


class CFConstraint(CFSyntax):
    def __init__(self, debug):
        super().__init__("constraint", debug)

    @staticmethod
    def parse(tokens, debug):
        constraint = CFConstraint(debug)
        constraint.enter_parser()

        current = tokens.current()
        if current.kind() is not TokenKind.IDENTIFIER:
            constraint.parser_error(current, TokenKind.IDENTIFIER)
        constraint_id = CFIdentifier.parse(tokens, debug)
        constraint._nonterms.append(constraint_id)

        current = tokens.current()
        if current.kind() is not TokenKind.FAT_ARROW:
            constraint.parser_error(current, TokenKind.FAT_ARROW)
        tokens.skip(TokenKind.FAT_ARROW)

        constraint.leave_parser()
        return constraint

    def pretty_print(self, file):
        pass
