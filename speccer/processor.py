# -*- coding: utf-8 -*-
from indentation import Indentation
from statement import Statements

def default_indentation():
    return 4 * ' '

class SpecificationProcessor:
    def __init__(self, file_name):
        self.file_name = file_name

        self._statements = Statements()

        self._test_found = False
        self._long_comment_found = False

    def process(self, lines):
        ret = ['import unittest', 'import ' + self.file_name]

        # check file beginning now (attach defs as is)
        # this is a bit weak since it allows defs to be only at beginning
        defs = map(lambda a: a.startswith('def'), lines)

        def r_index(a, val):
            # missing list.rindex...
            return len(a) - a[::-1].index(val) - 1

        first_index = 0
        if any(defs):
            last_def_index = r_index(defs, True)

            first_index = map(lambda a: a.strip(), lines[last_def_index:]).index('')
            first_index += last_def_index

        processed_lines = map(lambda a: self.process_line(a), lines[:first_index])
        ret.extend(processed_lines)

        test_class_name = 'Test' + self.file_name.capitalize()
        ret.append('class ' + test_class_name + '(unittest.TestCase):')

        new_lines, set_up = self.pick_set_up(lines[first_index:])

        for line in new_lines:
            processed_line = self.process_line(line, set_up)
            
            if processed_line:
                ret.append(processed_line)
        
        ret.extend(['suite = unittest.TestLoader().loadTestsFromTestCase(' + \
            test_class_name + ')',
            'unittest.TextTestRunner(verbosity=2).run(suite)'
        ])

        return '\n'.join(ret)

    def pick_set_up(self, lines):
        found_set_up = False
        new_lines = []
        set_up = []

        for line in lines:
            if line[0] == ' ':
                if found_set_up:
                    set_up.append(line)
                else:
                    new_lines.append(line)
            else:
                stripped_line = line.strip()
                if len(stripped_line) > 0:
                    if stripped_line == 'set up':
                        found_set_up = True
                    else:
                        new_lines.append(line)
                elif found_set_up:
                    found_set_up = False
                else:
                    new_lines.append(line)

        return new_lines, set_up

    def process_line(self, line, set_up=()):
        stripped_line = line.strip()

        if len(stripped_line) > 0 and stripped_line[0] == '#':
            return line

        skips = ('def', 'return')
        if any(map(lambda a: stripped_line.startswith(a + ' '), skips)):
            return line

        just_found = False
        if stripped_line.endswith("'''"):
            self._long_comment_found = '=' in stripped_line
            just_found = True

            if not self._long_comment_found:
                return line

        if not just_found and self._long_comment_found:
            return line

        if line and line[0] == ' ':
            indentation = Indentation(line)
            ret = self._statements.convert(stripped_line)

            if hasattr(ret, '__iter__'):
                return default_indentation() + indentation() + ret[0] + \
                    '\n' + default_indentation() + indentation() + ret[1]

            return (default_indentation() + indentation() + ret).rstrip()

        if len(stripped_line) > 0 and not self._test_found:
            self._test_found = True

            ret = '\n' + default_indentation() + 'def test_' + \
                stripped_line.replace(' ', '_') + '(self):'

            for content in set_up:
                ret += '\n' + default_indentation() + content

            return ret

        if not stripped_line or stripped_line == '\n':
            self._test_found = False

        return (default_indentation() + line).rstrip()
