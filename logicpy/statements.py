import itertools


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


class Not(Statement):

    def __init__(self, left):
        super().__init__(left, left)

    def __str__(self):
        return "¬{}".format(str(self.left))

    def get_value(self):
        return not self.left.get_value()


class TruthTable(object):

    def __init__(self, statement):
        self.statement = statement  # type: Statement

    def get_potential_variable_states(self):
        variables = self.statement.discover_variables()
        combos = []

        for i in range(len(variables)):
            combos += itertools.combinations(variables, i+1)
            
        states = [{var.name: False for var in variables}]

        for combo in combos:
            state = {}

            for var in combo:
                state[var.name] = True

            for var in variables:
                if var.name not in state:
                    state[var.name] = False

            states.append(state)
        return states

    def set_variable_states(self, states):
        variables = self.statement.discover_variables()

        for state in states:
            for variable in variables:
                if variable.name == state:
                    variable.set_value(states[state])

    def generate_states(self):
        states = []

        for state in self.get_potential_variable_states():

            self.set_variable_states(state)
            state["result"] = self.statement.get_value()
            states.append(state)

        return states
