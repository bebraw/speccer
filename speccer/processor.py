from indentation import Indentation

class SpecificationProcessor:
    def __init__(self, file_name):
        self.file_name = file_name

        self.found_set_up = False
        self.set_up_content = []

    def process(self, lines):
        ret = ['import ' + self.file_name, ]
        
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

            if '==' in line:
                return indentation() + 'assert ' + line.strip()
            elif 'raises' in line:
                expr, error = line.strip().split('raises')

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
