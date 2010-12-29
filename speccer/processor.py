# -*- coding: utf-8 -*-
from indentation import Indentation
from statement import Statements

def default_indentation():
    return 4 * ' '

class SpecificationProcessor:
    def __init__(self, file_name):
        self.file_name = file_name

        self._statements = Statements()

    def process(self, lines):
        test_class_name = 'Test' + self.file_name.capitalize()
        ret = ['import unittest', 'import ' + self.file_name,
            'class ' + test_class_name + '(unittest.TestCase):',
            ]

        new_lines, set_up = self.pick_set_up(lines)

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

        return new_lines, set_up

    def process_line(self, line, set_up=()):
        stripped_line = line.strip()

        if len(stripped_line) > 0 and stripped_line[0] == '#':
            return None

        if line[0] == ' ':
            indentation = Indentation(line)
            ret = self._statements.convert(stripped_line)

            if len(ret) == 0:
                return None
            elif hasattr(ret, '__iter__'):
                return default_indentation() + indentation() + ret[0] + \
                    '\n' + default_indentation() + indentation() + ret[1]

            return default_indentation() + indentation() + ret

        if len(stripped_line) > 0:
            if stripped_line.startswith('def '):
                return stripped_line

            ret = '\n' + default_indentation() + 'def test_' + \
                stripped_line.replace(' ', '_') + '(self):'

            for content in set_up:
                ret += '\n' + default_indentation() + content

            return ret
