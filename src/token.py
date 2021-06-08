class Token:
    def __init__(self, kind, line_no, value):
        self._kind = kind
        self._line_no = line_no
        self._value = value

    def get_kind(self):
        return self._kind

    def get_line_no(self):
        return self._line_no

    def get_value(self):
        return self._value

    def __str__(self):
        return f"\
Token: {self._kind.name}\n\
Line : {self._line_no}\n\
Value: '{self._value}'\n"
