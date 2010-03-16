from indentation import Indentation

def default_indentation():
    return 4 * ' '

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
        return l_part + ' ' + self.value + ' ' + r_part

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

class SpecificationProcessor:
    def __init__(self, file_name):
        self.file_name = file_name

        self._statements = Statements()
        self.found_set_up = False
        self.set_up_content = []

    def process(self, lines):
        test_class_name = 'Test' + self.file_name
        ret = ['import unittest', 'import ' + self.file_name,
            'class ' + test_class_name + '(unittest.TestCase):',
            ]
        
        for line in lines:
            processed_line = self.process_line(line)
            
            if processed_line:
                ret.append(processed_line)
        
        ret.extend(['suite = unittest.TestLoader().loadTestsFromTestCase(' + \
            test_class_name + ')',
            'unittest.TextTestRunner(verbosity=2).run(suite)'
        ])

        return '\n'.join(ret)

    # XXX: separate to LineProcessor?
    def process_line(self, line):
        stripped_line = line.strip()

        if len(stripped_line) > 0 and stripped_line[0] == '#':
            return None

        if line[0] == ' ':
            if self.found_set_up:
                self.set_up_content.append(line)
                return

            indentation = Indentation(line)
            ret = self._statements.convert(stripped_line)

            if len(ret) == 0:
                return None
            elif hasattr(ret, '__iter__'):
                return default_indentation() + indentation() + ret[0] + '\n' + \
                    default_indentation() + indentation() + ret[1]

            return default_indentation() + indentation() + ret

        if len(stripped_line) > 0:
            if stripped_line == 'set up':
                self.found_set_up = True
            else:
                ret = 'def test_' + stripped_line.replace(' ', '_') + '(self):'

                if len(self.set_up_content) > 0:
                    for content in self.set_up_content:
                        ret += '\n' + default_indentation() + content

                return '\n' + default_indentation() + ret
        elif self.found_set_up:
            self.found_set_up = False
