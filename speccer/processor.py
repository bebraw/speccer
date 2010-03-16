from indentation import Indentation
from statement import Statements

def default_indentation():
    return 4 * ' '

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
