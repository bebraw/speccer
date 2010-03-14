from __future__ import with_statement

import inspect
import imp
import os
import sys
import tempfile
from processor import SpecificationProcessor


class SpecificationRunner:
    def run(self, py_files):
        for py_file in py_files:
            spec_file = os.path.splitext(py_file)[0] + '.spec'

            if os.path.exists(spec_file):
                processor = SpecificationProcessor()

                with open(spec_file) as f:
                    lines = f.readlines()

                # TODO: set up imports!
                spec_code = processor.process(lines)

                # http://docs.python.org/library/tempfile.html#tempfile.mktemp
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
                tmp_file.write(spec_code)
                tmp_file.close()

                try:
                    module = imp.load_source('spec', tmp_file.name)
                except Exception, e:
                    os.unlink(tmp_file.name)
                    sys.exit(str(e))

                os.unlink(tmp_file.name)
                os.unlink(tmp_file.name + 'c')

                def to_dict(i):
                    ret = {}

                    for k, v in i:
                        ret[k] = v

                    return ret

                spec_funcs = inspect.getmembers(module, inspect.isfunction)
                spec_funcs = to_dict(spec_funcs)

                set_up = spec_funcs.get('set_up')
                for name, func in spec_funcs.items():
                    if name != 'set_up':
                        if set_up:
                            func(set_up()) # XXX: mod generated funcs to accept **kvargs
                        else:
                            func()

                # module_classes = inspect.getmembers(module, inspect.isclass)

                #spec_source = compile(spec_code, '<string>', 'exec')
                #exec(spec_source)

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
    py_files = ('myclass.py', 'processor.py')

    runner = SpecificationRunner()
    runner.run(py_files)
