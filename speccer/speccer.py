# -*- coding: utf-8 -*-
from __future__ import with_statement

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
                    try:
                        module = imp.load_source('spec', tmp_file.name)
                    except SystemExit:
                        pass
                except Exception, e:
                    os.unlink(tmp_file.name)
                    sys.exit(str(e))

                os.unlink(tmp_file.name)
                os.unlink(tmp_file.name + 'c')

if __name__ == "__main__":
    py_files = ('indentation.py', 'myclass.py', 'processor.py')

    runner = SpecificationRunner()
    runner.run(py_files)
