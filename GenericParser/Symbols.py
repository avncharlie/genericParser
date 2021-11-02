# Classes used to represent production rules

class nonTerminal:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

class terminal:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        if isinstance(other, terminal):
            return self.name == other.name
        return False

class grammar_or:
    def __init__(self, *args):
        self.items = [*args]

    def __repr__(self):
        return '(' + ''.join([ str(x) + " | " for x in self.items ])[:-3] + ')'

class grammar_seq:
    def __init__(self, *args):
        self.items = [*args]

    def __repr__(self):
        return '(' + ''.join([ str(x) + " " for x in self.items ])[:-3] + ')'


