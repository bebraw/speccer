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
            py_file_name = os.path.splitext(py_file)[0]
            spec_file = py_file_name + '.spec'

            if os.path.exists(spec_file):
                processor = SpecificationProcessor(py_file_name)

                with open(spec_file) as f:
                    lines = f.readlines()

                spec_code = processor.process(lines)
                #print spec_code

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
                    func()

if __name__ == "__main__":
    py_files = ('myclass.py', 'processor.py')

    runner = SpecificationRunner()
    runner.run(py_files)
