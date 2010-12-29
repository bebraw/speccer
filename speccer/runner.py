# -*- coding: utf-8 -*-
from __future__ import with_statement

import glob
import imp
import os
import sys
import tempfile
from optparse import OptionParser
from processor import SpecificationProcessor

import version

class SpecificationRunner:
    def run(self, spec_files):
        for spec_file_name in spec_files:
            base_name = os.path.splitext(spec_file_name)[0]
            py_file_name = base_name + '.py'

            if os.path.exists(py_file_name):
                print('\n**Testing ' + spec_file_name + '**\n')

                processor = SpecificationProcessor(base_name)

                with open(spec_file_name) as f:
                    lines = f.readlines()

                spec_code = processor.process(lines)

                # http://docs.python.org/library/tempfile.html#tempfile.mktemp
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
                tmp_file.write(spec_code)
                tmp_file.close()

                try:
                    try:
                        module = imp.load_source('spec', tmp_file.name)
                    except SystemExit:
                        print('Module ' + base_name + ' not found!');
                except Exception, e:
                    os.unlink(tmp_file.name)
                    sys.exit(str(e))

                os.unlink(tmp_file.name)
                os.unlink(tmp_file.name + 'c')

def get_specs():
    return glob.glob('*.spec')

def output_tests(*args):
    pass # TODO!

def run_tests(spec_files):
    if len(spec_files) == 0:
        print('\nNo specifications found!')

        return False
    else:
        print('\nRunning tests')

        runner = SpecificationRunner()
        runner.run(spec_files)

        return True

def looping_run(*args):
    def get_file_times(filenames):
        get_file_time = lambda filename: os.stat(filename).st_mtime

        return map(get_file_time, filenames)

    specs = get_specs()
    tests_found = run_tests(specs)

    if not tests_found:
        return

    file_times = get_file_times(specs)

    while True:
        new_file_times = get_file_times(specs)

        if file_times != new_file_times:
            file_times = new_file_times

            run_tests(specs)

def show_version(*args):
    print("speccer %s" % version.get())
    sys.exit(0)

def main():
    # make sure current working directory is in the path
    # this is needed for imports to work
    cwd = os.getcwd()
    sys.path.append(cwd)

    usage = """usage: %prog command [args] [options]"""

    description = """Brief Description:
Speccer is a specification based test runner."""

    epilog = """\nLong Description:
Speccer is a specification based test runner. It uses a special syntax to wrap
Python's native unittest module. Tests are defined like this:

myclass.spec (tests myclass.py):
set up
    c = myclass.MyClass()

adds two and two
    c.add(2,2) == 4

adds negatives
    c.add(10, -10) == 0

fails adding int and string
    c.add(10, 'foo') raises TypeError

As you can see the syntax is quite light. It's pretty much like regular Python
but with less noise. Asserts and function definitions are implicit.

In order to run the tests, just run the tool without any parameters in the
folder they are in."""

    class MyParser(OptionParser):
        def format_epilog(self, formatter):
            return self.epilog

    parser = MyParser(usage=usage, description=description, epilog=epilog)
    parser.add_option("-v", "--version", action="callback",
        callback=show_version,
        help="show program's version number and exit")
    parser.add_option("-l", "--loop", action="callback",
        callback=looping_run,
        help="run tests in a looping manner. Tests get run each time a spec file is changed")
    parser.add_option("-o", "--output", action="callback",
        callback=output_tests,
        help="output generated test files to given folder")

    parser.parse_args()

    if sys.argv < 2:
        run_tests(get_specs())

if __name__ == '__main__':
    main()
