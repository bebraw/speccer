from indentation import Indentation

class SpecificationProcessor:
    def __init__(self, file_name):
        self.file_name = file_name

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
        
        #ret.append('main()')
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
            indentation = Indentation(line)
            ret = None

            if self.found_set_up:
                self.set_up_content.append(line)
                return

            if '==' in stripped_line:
                parts = stripped_line.split('==')
                parts = [part.strip() for part in parts]
                parts_len = len(parts)
                parts_lim = int(round(parts_len / 2.0))

                l_part = '=='.join(parts[0:parts_lim])
                r_part = '=='.join(parts[parts_lim:parts_len])

                ret = indentation() + 'self.assertEqual(' + l_part + ', ' + \
                    r_part + ')'
            elif '!=' in stripped_line:
                parts = stripped_line.split('!=')
                parts = [part.strip() for part in parts]
                parts_len = len(parts)
                parts_lim = int(round(parts_len / 2.0))

                l_part = '!='.join(parts[0:parts_lim])
                r_part = '!='.join(parts[parts_lim:parts_len])

                ret = indentation() + 'self.assertNotEqual(' + l_part + ', ' + \
                    r_part + ')'
            elif 'raises' in stripped_line:
                expr, error = stripped_line.split('raises')

                ret = indentation() + 'try: ' + expr + '\n' + \
                    self._default_indentation + indentation() + 'except ' + \
                    error + ': pass'
            elif len(stripped_line) == 0:
                return None
            else:
                ret = line

            return self._default_indentation + ret

        if len(stripped_line) > 0:
            if stripped_line == 'set up':
                self.found_set_up = True
            else:
                ret = 'def test_' + stripped_line.replace(' ', '_') + '(self):'

                if len(self.set_up_content) > 0:
                    for content in self.set_up_content:
                        ret += '\n' + self._default_indentation + content

                return '\n' + self._default_indentation + ret
        elif self.found_set_up:
            self.found_set_up = False

    @property
    def _default_indentation(self):
        return 4 * ' '
