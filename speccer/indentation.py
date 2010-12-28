# -*- coding: utf-8 -*-
class Indentation:
    def __init__(self, line):
        indentation_end = self._find_last_from_beginning(line, ' ')
        self.amount = indentation_end + 1

    def _find_last_from_beginning(self, line, needle):
        for i, char in enumerate(line):
            if char != needle:
                return i - 1

        return 0

    def __call__(self):
        return self.amount * ' '
