class Statement(object):

    def __init__(self, left=None, right=None):
        self.left = left  # type: Statement
        self.right = right  # type: Statement

    def __add__(self, other):
        return OrStatement(self, other)

    def __mul__(self, other):
        return AndStatement(self, other)

    def get_value(self):
        return True


class AndStatement(Statement):

    def get_value(self):
        return self.left.get_value() and self.right.get_value()


class OrStatement(Statement):

    def get_value(self):
        return self.left.get_value() or self.right.get_value()


class Variable(Statement):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.value = False

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value
