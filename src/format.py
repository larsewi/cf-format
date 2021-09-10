from exceptions import CFSyntaxException
from pretty import Pretty


class Format:
    def __init__(self):
        self.tokens = []
        self.tokidx = 0
        self.toklen = 0
        self.pretty = None

    def input(self, tokens):
        self.tokens = tokens
        self.tokidx = 0
        self.toklen = len(tokens)
        self.pretty = Pretty()
        self.f_policy()

    def __str__(self):
        return self.pretty.__str__()

    def empty(self):
        return True if self.tokidx >= self.toklen else False

    def peek(self):
        if self.empty():
            raise CFSyntaxException("Unexpectedly reached end of file")
        return self.tokens[self.tokidx]

    def pop(self, *expected):
        token = self.peek()
        self.tokidx += 1

        if expected and token.type not in expected:
            msg = "Expected "
            first = True
            for expect in expected:
                if first:
                    first = False
                else:
                    msg += ", "
                msg += expect.lower().replace("_", " ")
            msg += "; found %s" % token.__str__()
            raise CFSyntaxException(msg)

        return token

    def push_back(self, n=1):
        assert self.tokidx - n >= 0
        self.tokidx -= n

    def f_policy(self):
        last = None
        while not self.empty():
            token = self.pop("BUNDLE", "BODY", "PROMISE", "COMMENT", "MACRO")

            if not (last and last.type == "COMMENT" and token.lineno - last.lineno == 1):
                self.pretty.println()

            if token.type == "BUNDLE":
                self.push_back()
                self.f_bundle_block()
            elif token.type == "BODY":
                self.push_back()
                self.f_body_block()
            elif token.type == "PROMISE":
                self.push_back()
                self.f_promise_block()
            elif token.type == "COMMENT":
                self.pretty.print(token.value)
            elif token.type == "MACRO":
                self.pretty.print(token.value)
            else:
                assert False

            self.pretty.println()
            last = token

    def f_bundle_block(self):
        stash = []

        # print bundle
        token = self.pop("BUNDLE")
        self.pretty.print(token.value)

        macro_found = self.f_print_macros_stash_comments(stash)

        # print space
        if not macro_found:
            self.pretty.print(" ")

        # print bundletype
        token = self.pop("IDENTIFIER")
        self.pretty.print(token.value)

        macro_found = self.f_print_macros_stash_comments(stash)

        # print space
        if not macro_found:
            self.pretty.print(" ")

        # print bundleid
        token = self.pop("IDENTIFIER")
        self.pretty.print(token.value)

        self.f_print_macros_stash_comments(stash)

        # print arglist
        self.f_arglist()


    def f_body_block(self):
        pass

    def f_promise_block(self):
        pass

    def f_arglist(self):
        stash = []

        # print left parenthesis
        token = self.pop("LEFT_PARENTHESIS")
        self.pretty.print(token.value)

        if not self.f_arglist_no_wrap(stash):
            if not self.f_arglist_single_wrap(stash):
                self.f_arglist_full_wrap(stash)

        # print right parenthesis
        token = self.pop("RIGHT_PARENTHESIS")
        self.pretty.print(token.value)

    def f_arglist_no_wrap(self, stash):
        rev_tok = 0
        rev_cur = self.pretty.get_cursor()
        tmp_stash = []

        last = None
        while self.peek().type != "RIGHT_PARENTHESIS":
            # stash comment
            if self.peek().type == "COMMENT":
                stash.append(self.pop())
                rev_tok += 1
            # print identifier
            elif not last or last.type == "COMMA":
                # print space in front of identifier
                if last:
                    self.pretty.print(" ")
                token = self.pop("IDENTIFIER", "COMMENT", "MACRO")
                rev_tok += 1
                self.pretty.print(token.value)
                last = token
            # print comma
            elif last and last.type == "IDENTIFIER":
                token = self.pop("COMMA", "COMMENT", "MACRO")
                rev_tok += 1
                self.pretty.print(token.value)
                last = token
            else:
                msg = "Expected identifier, comment, macro; found %s" % self.peek().__str__()
                raise CFSyntaxException(msg)

            # no wrap failed, revert back and return failure
            if self.pretty.should_wrap(1) or self.peek() == "MACRO":
                self.pretty.truncate_to(rev_cur)
                self.push_back(rev_tok)
                return False

        # TODO - if last is comma, remove it

        stash.extend(tmp_stash)
        return True

    def f_arglist_single_wrap(self, stash):
        rev_tok = 0
        rev_cur = self.pretty.get_cursor()
        tmp_stash = []

        self.pretty.indent()
        self.pretty.println()

        last = None
        while self.peek().type != "RIGHT_PARENTHESIS":
            # stash comment
            if self.peek().type == "COMMENT":
                stash.append(self.pop())
                rev_tok += 1
            # print identifier
            elif not last or last.type == "COMMA":
                # print space in front of identifier
                if last:
                    self.pretty.print(" ")
                token = self.pop("IDENTIFIER", "COMMENT", "MACRO")
                rev_tok += 1
                self.pretty.print(token.value)
                last = token
            # print comma
            elif last and last.type == "IDENTIFIER":
                token = self.pop("COMMA", "COMMENT", "MACRO")
                rev_tok += 1
                self.pretty.print(token.value)
                last = token
            else:
                msg = "Expected identifier, comment, macro; found %s" % self.peek().__str__()
                raise CFSyntaxException(msg)

            # no wrap failed, revert back and return failure
            if self.pretty.should_wrap(1) or self.peek() == "MACRO":
                self.pretty.truncate_to(rev_cur)
                self.push_back(rev_tok)
                return False
        
        # TODO - if last is comma, remove it

        self.pretty.println()
        self.pretty.dedent()

        stash.extend(tmp_stash)
        return True

    def f_arglist_full_wrap(self, stash):
        local_stash = []

        self.pretty.indent()
        self.pretty.println()

        last = None
        while self.peek().type != "RIGHT_PARENTHESIS":
            if self.peek().type == "COMMENT":
                if last and last.type == "COMMA":
                    self.pretty.print("  ")
                    self.pretty.print(self.pop().value)
                else:
                    local_stash.append(self.pop())
            elif self.peek().type == "MACRO":
                self.pretty.println()
                self.pretty.print_no_indent(self.pop().value)
                self.pretty.println()
            elif not last and last.type == "COMMA":
                pass # identifier
            elif last and last.type == "IDENTIFIER":
                pass # comma

        # TODO -  add comma if not comma last

        self.pretty.println()
        self.pretty.dedent()

    def f_print_macros_stash_comments(self, stash):
        macro_found = False
        while not self.empty() and self.peek().type in ("COMMENT", "MACRO"):
            if self.peek().type == "COMMENT":
                stash.append(self.pop())
            else:
                self.pretty.println()
                self.pretty.print_no_indent(self.pop())
                self.pretty.println()
                macro_found = True
        return macro_found


