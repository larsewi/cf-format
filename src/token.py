class Token:
    def __init__(self, kind, value, filename, line, line_no, column):
        self._kind = kind
        self._value = value
        self._filename = filename
        self._line = line
        self._line_no = line_no
        self._column = column

    def kind(self):
        return self._kind

    def value(self):
        return self._value

    def filename(self):
        return self._filename

    def line(self):
        return self._line

    def line_no(self):
        return self._line_no
    
    def column(self):
        return self._column

    def __str__(self):
        return f"\
Token   : {self._kind.name}\n\
Line no : {self._line_no}\n\
Column  : {self._column}\n\
Value   : '{self._value}'\n"
