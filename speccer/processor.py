# -*- coding: utf-8 -*-
from functools import partial
from string import strip
from indentation import Indentation
from statement import Statements

def default_indentation():
    return 4 * ' '

def first_test_index(lines):
    def is_ok(i):
        a = i[1]
        return not any(map(a.startswith, ('def', ' ', '#'))) and ('=' not in a) and len(a) > 1

    try:
        return filter(is_ok, enumerate(lines))[0][0]
    except IndexError:
        return 0

class SpecificationProcessor:
    def __init__(self, file_name):
        self.file_name = file_name

        self._statements = Statements()

        self._test_found = False
        self._long_comment_found = False

    def process(self, lines):
        ret = []

        if len(filter(bool, map(strip, lines))) == 0:
            return ''

        # note that this assumes defs and assignments are at the beginning,
        # possible set up next and actual tests after that

        i = first_test_index(lines)
        ret.extend(lines[:i])

        new_lines, set_up = self.pick_set_up(lines[i:])

        if len(new_lines):
            ret.extend(['import unittest', 'import ' + self.file_name])

            test_class_name = 'Test' + self.file_name.capitalize()
            ret.append('class ' + test_class_name + '(unittest.TestCase):')

            ret.extend(filter(bool, map(partial(self.process_line, set_up=set_up), new_lines)))

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
