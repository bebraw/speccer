# -*- coding: utf-8 -*-
from functools import partial
from string import strip
from indentation import Indentation
from statement import Statements
from utils import OrderedDict


def default_indentation():
    return 4 * ' '

def first_test_index(lines):
    def is_ok(i):
        a = i[1]
        return not any(map(a.startswith, ('def ', ' ', '#', 'from ', 'import ', 'print '))) and ('=' not in a) and len(a) > 1

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
        if len(filter(bool, map(strip, lines))) == 0:
            return ''

        blocks = self._parse_blocks(lines)

        ret = []

        ret.extend(['import unittest',
            'try:\n    import ' + self.file_name + '\nexcept ImportError: pass'])

        ret.extend(blocks.imports)

        ret.extend(blocks.assignments)
        ret.extend(blocks.defs)

        if blocks.tests:
            test_class_name = 'Test' + self.file_name.capitalize()
            ret.append('class ' + test_class_name + '(unittest.TestCase):')

            ret.extend(self._process_lines(blocks.tests, blocks.set_up[1:]))

            ret.extend(['\nsuite = unittest.TestLoader().loadTestsFromTestCase(' + \
                test_class_name + ')',
                'unittest.TextTestRunner(verbosity=2).run(suite)'
            ])

        return '\n'.join(ret)

    def _parse_blocks(self, lines):
        class Blocks:
            def __init__(self):
                self.imports = []
                self.assignments = []
                self.defs = []
                self.set_up = []
                self.tests = []

            def add(self, target, accum):
                try:
                    a = getattr(self, target)

                    a.extend(accum)
                except AttributeError:
                    pass

        blocks = Blocks()

        def begins_with(name):
            return lambda begin, line: begin == name

        def exact(name):
            return lambda begin, line: line.rstrip() == name

        patterns = OrderedDict([
            (begins_with('def'), 'defs'),
            (begins_with('import'), 'imports'),
            (begins_with('from'), 'imports'),
            (exact('set up'), 'set_up'),
            (lambda begin, line: begin and '=' in line and begin != ' ', 'assignments'),
            (lambda begin, line: begin != ' ' and begin != '' and begin != '\n', 'tests'),
        ])

        def match(line):
            begin = line.split(' ')[0]

            for k, v in patterns.items():
                if k(begin, line):
                    return v

        def accumulate(line):
            matched = match(line)

            if matched:
                blocks.add(accumulate.target, accumulate.items)
                accumulate.target = matched
                accumulate.items = []

            accumulate.items.append(line)

        accumulate.target = ''
        accumulate.items = []

        map(accumulate, lines)
        blocks.add(accumulate.target, accumulate.items)

        return blocks

    def _process_lines(self, lines, set_up=()):
        return filter(bool, map(partial(self.process_line, set_up=set_up), lines))

    def pick_set_up(self, lines):
        found_set_up = False
        new_lines = []
        set_up = []

        for line in lines:
            if len(line) > 0 and line[0] == ' ':
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
