# -*- coding: utf-8 -*-
from string import strip


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
        return l_part + ', ' + r_part if r_part else l_part

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

class In(Statement):
    value = ' in '
    code = 'assertIn'

    def matches(self, line):
        return not line.strip().startswith('for ') and self.value in line

class NotIn(Statement):
    value = ' not in '
    code = 'assertNotIn'

class Is(Statement):
    value = ' is '
    code = 'assertIs'

class IsNot(Statement):
    value = ' is not '
    code = 'assertIsNot'

class IsNotNone(Statement):
    value = ' is not None'
    code = 'assertIsNotNone'

class IsNone(Statement):
    value = ' is None'
    code = 'assertIsNone'

class IsNotInstance(Statement):
    value = ' is not instanceof '
    code = 'assertNotIsInstance'

class IsInstance(Statement):
    value = ' is instanceof '
    code = 'assertIsInstance'

def _convert(line, split_char, assertion):
    parts = map(strip, line.split(split_char))
    ret = ''

    for l, r in zip(parts, parts[1:]):
        l = l.strip('=').strip()
        op = assertion
 
        if r.startswith('='):
            op += 'Equal'
            r = r.strip('=').strip()

        ret += 'self.assert' + op + '(' + l + ', ' + r + ');'

    return ret

class MultipleGreater(Statement):
    def matches(self, line):
        return bool(line.count('>') > 1)

    def convert(self, line):
        return _convert(line, '>', 'Greater')

class MultipleLesser(Statement):
    def matches(self, line):
        return bool(line.count('<') > 1)

    def convert(self, line):
        return _convert(line, '<', 'Less')

class GreaterThan(Statement):
    value = '>'
    code = 'assertGreater'

class GreaterThanOrEquals(Statement):
    value = '>='
    code = 'assertGreaterEqual'

class LessThan(Statement):
    value = '<'
    code = 'assertLess'

class LessThanEquals(Statement):
    value = '<='
    code = 'assertLessEqual'

class Any(Statement):
    def matches(self, line):
        return True

    def convert(self, line):
        return line

class Statements(list):
    def __init__(self):
        statements = (Equals(), NotEquals(), AlmostNotEquals(),
            AlmostEquals(),
            MultipleGreater(), MultipleLesser(),
            GreaterThanOrEquals(), GreaterThan(),
            LessThanEquals(), LessThan(), Raises(),
            IsNotInstance(), IsInstance(),
            NotIn(), In(), IsNotNone(), IsNone(),
            IsNot(), Is(), Any(), )

        super(Statements, self).__init__(statements)

    def convert(self, line):
        for statement in self:
            if statement.matches(line):
                return statement.convert(line)
