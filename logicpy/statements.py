class Statement(object):

    def __init__(self, left=None, right=None):
        self.left = left  # type: Statement
        self.right = right  # type: Statement

    def __add__(self, other):
        return OrStatement(self, other)

    def __mul__(self, other):
        return AndStatement(self, other)

    def __gt__(self, other):
        return ImpliesStatement(self, other)

    def discover_variables(self):
        if isinstance(self, Variable):
            return {self}
        else:
            return self.left.discover_variables() | self.right.discover_variables()

    def get_value(self):
        return True


class AndStatement(Statement):

    def __str__(self):
        return "({} ∧ {})".format(str(self.left), str(self.right))

    def get_value(self):
        return self.left.get_value() and self.right.get_value()


class OrStatement(Statement):

    def __str__(self):
        return "({} ∨ {})".format(str(self.left), str(self.right))

    def get_value(self):
        return self.left.get_value() or self.right.get_value()


class ImpliesStatement(Statement):

    def __str__(self):
        return "({} → {})".format(str(self.left), str(self.right))

    def get_value(self):
        return not self.left.get_value() or (self.left.get_value() and self.right.get_value())


class Variable(Statement):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.value = False

    def __str__(self):
        return self.name

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value
