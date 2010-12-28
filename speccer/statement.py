# -*- coding: utf-8 -*-
class Statement:
    def matches(self, line):
        return self.value in line

    def convert(self, line):
        parts = line.split(self.value)
        parts = [part.strip() for part in parts]
        parts_len = len(parts)
        parts_lim = int(round(parts_len / 2.0))

        l_part = self.value.join(parts[0:parts_lim])
        r_part = self.value.join(parts[parts_lim:parts_len])

        code_params = self._code_parameters(l_part, r_part)
        return 'self.' + self.code + '(' + code_params + ')'

    def _code_parameters(self, l_part, r_part):
        return l_part + ', ' + r_part

class Equals(Statement):
    value = '=='
    code = 'assertEqual'

class NotEquals(Statement):
    value = '!='
    code = 'assertNotEqual'

class AlmostEquals(Statement):
    value = '~='
    code = 'assertAlmostEqual'

class AlmostNotEquals(Statement):
    value = '!~='
    code = 'assertNotAlmostEqual'

class Raises(Statement):
    value = 'raises'

    def convert(self, line):
        expr, error = line.split('raises')

        return ['try:' + expr, 'except' + error + ': pass']

class Inequality(Statement):
    code = 'assertTrue'

    def _code_parameters(self, l_part, r_part):
        l_parts = l_part.split(self.value)

        return (' ' + self.value + ' ').join(l_parts) + ' ' + self.value + \
            ' ' + r_part

class BiggerThan(Inequality):
    value = '>'

class BiggerThanOrEquals(Inequality):
    value = '>='

class SmallerThan(Inequality):
    value = '<'

class SmallerThanEquals(Inequality):
    value = '<='

class Any(Statement):
    def matches(self, line):
        return True

    def convert(self, line):
        return line

class Statements(list):
    def __init__(self):
        statements = (Equals(), NotEquals(), AlmostNotEquals(),
            AlmostEquals(), BiggerThanOrEquals(), BiggerThan(),
            SmallerThanEquals(), SmallerThan(), Raises(), Any())

        super(Statements, self).__init__(statements)

    def convert(self, line):
        for statement in self:
            if statement.matches(line):
                return statement.convert(line)
