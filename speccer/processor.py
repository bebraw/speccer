from indentation import Indentation

class SpecificationProcessor:
    def __init__(self, file_name):
        self.file_name = file_name

        self.found_set_up = False
        self.set_up_content = []

    def process(self, lines):
        ret = ['import ' + self.file_name, 'from expecter import expect', ]
        
        for line in lines:
            processed_line = self.process_line(line)
            
            if processed_line:
                ret.append(processed_line)
        
        return '\n'.join(ret)

    # XXX: separate to LineProcessor?
    def process_line(self, line):
        stripped_line = line.strip()

        if len(stripped_line) > 0 and stripped_line[0] == '#':
            return None

        if line[0] == ' ':
            indentation = Indentation(line)

            if self.found_set_up:
                self.set_up_content.append(line)
                return

            if '==' in stripped_line:
                parts = stripped_line.split('==')
                parts_len = len(parts)

                l_part = '=='.join(parts[0:parts_len/2])
                r_part = '=='.join(parts[parts_len/2:parts_len])
                return indentation() + 'expect(' + l_part + ') == ' + r_part
            elif 'raises' in stripped_line:
                expr, error = stripped_line.split('raises')

                return indentation() + 'try: ' + expr + '\n' + \
                    indentation() + 'except ' + error + ': pass'
            else:
                return line

        if len(stripped_line) > 0:
            if stripped_line == 'set up':
                self.found_set_up = True
            else:
                ret = 'def ' + stripped_line.replace(' ', '_') + '():'

                if len(self.set_up_content) > 0:
                    for content in self.set_up_content:
                        ret += '\n' + content

                return ret
        elif self.found_set_up:
            self.found_set_up = False
