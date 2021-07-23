from cf_arglist import CFArgList
from cf_bundlebody import CFBundleBody
from cf_comment import CFComment
from cf_identifier import CFIdentifier
from cf_syntax import CFSyntax
from token import TokenKind


class CFBundle(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundle", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        bundle = CFBundle(debug)
        bundle.enter_parser()

        tokens.skip(TokenKind.BUNDLE)

        CFComment.parse_while(bundle, tokens, debug)

        current = tokens.current()
        if current.kind() is not TokenKind.IDENTIFIER:
            bundle.parser_error(current, TokenKind.IDENTIFIER)
        bundletype = CFIdentifier.parse(tokens, debug)
        assert bundletype is not None
        bundle._nonterms.append(bundletype)

        CFComment.parse_while(bundle, tokens, debug)

        current = tokens.current()
        if current.kind() is not TokenKind.IDENTIFIER:
            bundle.parser_error(current, TokenKind.IDENTIFIER)
        bundleid = CFIdentifier.parse(tokens, debug)
        assert bundleid is not None
        bundle._nonterms.append(bundleid)

        CFComment.parse_while(bundle, tokens, debug)

        current = tokens.current()
        if current.kind() is TokenKind.LEFT_PAR:
            arglist = CFArgList.parse(tokens, debug)
            assert arglist is not None
            bundle._nonterms.append(arglist)

        CFComment.parse_while(bundle, tokens, debug)

        current = tokens.current()
        if current.kind() is not TokenKind.LEFT_BRACE:
            bundle.parser_error(current, TokenKind.IDENTIFIER)
        bundlebody = CFBundleBody.parse(tokens, debug)
        assert bundlebody is not None
        bundle._nonterms.append(bundlebody)

        bundle.leave_parser()
        return bundle

    def pretty_print(self, file):
        pass
