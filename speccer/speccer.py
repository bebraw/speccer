from __future__ import with_statement

import imp
import os
from processor import SpecificationProcessor


class SpecificationRunner:
    def run(self, py_files):
        for py_file in py_files:
            spec_file = os.path.splitext(py_file)[0] + '.spec'

            if os.path.exists(spec_file):
                processor = SpecificationProcessor()

                with open(spec_file) as f:
                    lines = f.readlines()

                spec_code = processor.process(lines)
                # XXX: add testing part to the the code! alternatively the
                # file could be output to a temp file and then imported via imp
                # in that case inspect can be used!
                spec_source = compile(spec_code, '<string>', 'exec')
                exec(spec_source)

                specs = {}

                for k, v in specs.items():
                    if k != 'set up':
                        if ' raises ' in v:
                            test_code, exc = v.split(' raises ')

                            try:
                                self.run_test(set_up, module_name, module, test_code)
                            except eval(exc):
                                pass
                        else:
                            self.run_test(set_up, module_name, module, v)

    def run_test(self, set_up, module_name, module, test_code):
        # TODO: replace this with something nicer :) (ie. expecter or specs)
        test = set_up + ';assert ' + test_code
        exec(test, {module_name: module, })


if __name__ == "__main__":
    imp_files = ('myclass.py', 'processor.py')

    runner = SpecificationRunner()
    runner.run(imp_files)
