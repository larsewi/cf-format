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
        nonterms = bundle._nonterms

        tokens.skip(TokenKind.BUNDLE)

        # Parse comments if any
        while tokens.current().kind() is TokenKind.COMMENT:
            comment = CFComment.parse(tokens, debug)
            assert comment is not None
            nonterms.append(comment)

        # Parse bundletype
        current = tokens.current()
        if current.kind() is not TokenKind.IDENTIFIER:
            bundle.parser_error(current, TokenKind.IDENTIFIER)
        bundletype = CFIdentifier.parse(tokens, debug)
        assert bundletype is not None
        nonterms.append(bundletype)

        # Parse comments if any
        while tokens.current().kind() is TokenKind.COMMENT:
            comment = CFComment.parse(tokens, debug)
            assert comment is not None
            nonterms.append(comment)

        # Parse bundleid
        current = tokens.current()
        if current.kind() is not TokenKind.IDENTIFIER:
            bundle.parser_error(current, TokenKind.IDENTIFIER)
        bundleid = CFIdentifier.parse(tokens, debug)
        assert bundleid is not None
        nonterms.append(bundleid)

        # Parse comments if any
        while tokens.current().kind() is TokenKind.COMMENT:
            comment = CFComment.parse(tokens, debug)
            assert comment is not None
            nonterms.append(comment)

        # Parse arglist
        if tokens.current().kind() is TokenKind.LEFT_PAR:
            arglist = CFArgList.parse(tokens, debug)
            assert arglist is not None
            nonterms.append(arglist)

        # Parse comments if any
        while tokens.current().kind() is TokenKind.COMMENT:
            comment = CFComment.parse(tokens, debug)
            assert comment is not None
            nonterms.append(comment)

        # Parse bundlebody
        bundlebody = CFBundleBody.parse(tokens, debug)
        assert bundlebody is not None
        nonterms.append(bundlebody)

        bundle.leave_parser()
        return bundle

    def pretty_print(self, cursor=0):
        nonterms = self._nonterms
        s = "bundle "
        cursor += len(s)
        buf = s

        while isinstance(nonterms[0], CFComment):
            comment = nonterms.pop(0)
            buf += comment.pretty_print() + "\n"
            cursor = 0
        
        bundletype = nonterms.pop(0)
        assert isinstance(bundletype, CFIdentifier)
        s = bundletype.pretty_print() + " "
        cursor += len(s)
        buf += s

        while isinstance(nonterms[0], CFComment):
            comment = nonterms.pop(0)
            buf += comment.pretty_print() + "\n"
            cursor = 0

        bundleid = nonterms.pop(0)
        assert isinstance(bundleid, CFIdentifier)
        s = bundleid.pretty_print()
        cursor += len(s)
        buf += s

        while isinstance(nonterms[0], CFComment):
            comment = nonterms.pop(0)
            buf += comment.pretty_print() + "\n"
            cursor = 0

        if isinstance(nonterms[0], CFArgList):
            arglist = nonterms.pop(0)
            buf += arglist.pretty_print(cursor) + "\n"
            cursor = 0

        while isinstance(nonterms[0], CFComment):
            comment = nonterms.pop(0)
            buf += comment.pretty_print() + "\n"
            cursor = 0

        bundlebody = nonterms.pop(0)
        assert isinstance(bundlebody, CFBundleBody)
        buf += bundlebody.pretty_print()

        return buf
