from cf_arglist import CFArgList
from cf_bundlebody import CFBundleBody
from cf_identifier import CFIdentifier
from cf_comment import CFComment
from cf_macro import CFMacro
from cf_syntax import CFSyntax
from token import TokenKind as tk


class CFBundle(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundle", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        bundle = CFBundle(debug)
        bundle.enter_parser()

        tokens.skip(tk.BUNDLE)

        # Parse comments and macros
        bundle.parse_while(tokens, debug, {tk.COMMENT: CFComment, tk.MACRO: CFMacro})

        # Parse bundletype
        bundle.parse_or_error(tokens, debug, {tk.IDENTIFIER: CFIdentifier})

        # Parse comments and macros
        bundle.parse_while(tokens, debug, {tk.COMMENT: CFComment, tk.MACRO: CFMacro})

        # Parse bundleid
        bundle.parse_or_error(tokens, debug, {tk.IDENTIFIER: CFIdentifier})

        # Parse comments and macros
        bundle.parse_while(tokens, debug, {tk.COMMENT: CFComment, tk.MACRO: CFMacro})

        # Parse arglist
        bundle.parse_if(tokens, debug, {tk.LEFT_PAR: CFArgList})

        # Parse comments and macros
        bundle.parse_while(tokens, debug, {tk.COMMENT: CFComment, tk.MACRO: CFMacro})

        # Parse bundlebody
        bundle.push(CFBundleBody.parse(tokens, debug))

        bundle.leave_parser()
        return bundle

    def pretty_print(self, pp):
        stash = []

        pp.print("bundle")
        pp.print(" ")

        # Comment / macro
        while isinstance(self.peek(), (CFComment, CFMacro)):
            if isinstance(self.peek(), CFComment):
                stash.append(self.pop())
            else:
                pp.println()
                self.pop().pretty_print(pp)
                pp.println()

        # Bundletype
        assert isinstance(self.peek(), CFIdentifier)
        self.pop().pretty_print(pp)
        pp.print(" ")

        # Comment / macro
        while isinstance(self.peek(), (CFComment, CFMacro)):
            if isinstance(self.peek(), CFComment):
                stash.append(self.pop())
            else:
                self.pop().pretty_print(pp)

        # Bundleid
        assert isinstance(self.peek(), CFIdentifier)
        self.pop().pretty_print(pp)

        # Comment / macro
        while isinstance(self.peek(), (CFComment, CFMacro)):
            if isinstance(self.peek(), CFComment):
                stash.append(self.pop())
            else:
                self.pop().pretty_print(pp)

        # Arglist
        if isinstance(self.peek(), CFArgList):
            self.pop().pretty_print(pp)

        # Print stashed comments
        for comment in stash:
            pp.print("  ")
            comment.pretty_print(pp)

        # Print trailing comment
        if isinstance(self.peek(), CFComment):
            if self.peek().column() > 0:
                # We assume this is a trailing comment. Information is lost
                # due to skipping RIGHT_PAR in parsing ArgList.
                pp.print("  ")
                self.pop().pretty_print(pp)
        pp.println()

        # Comment / macro
        while isinstance(self.peek(), (CFComment, CFMacro)):
            self.pop().pretty_print(pp)
            pp.println()

        # Bundlebody
        assert isinstance(self.peek(), CFBundleBody)
        self.pop().pretty_print(pp)
