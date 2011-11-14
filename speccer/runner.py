# -*- coding: utf-8 -*-
from __future__ import with_statement

import glob
import imp
import os
import sys
import tempfile
import time
from optparse import OptionParser
from processor import SpecificationProcessor
from itertools import chain

import __init__


def get_base_name(a):
    return os.path.splitext(a)[0]

def run(spec_files):
    for spec_file_name in spec_files:
        base_name = get_base_name(spec_file_name)
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

def output_tests(option, opt, output_dir, parser):
    got_all = False

    for spec_name in get_specs():
        with open(spec_name) as f:
            lines = f.readlines()

        base_name = get_base_name(spec_name)
        processor = SpecificationProcessor(base_name)
        spec_code = processor.process(lines)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        py_file_name = 'test_' + base_name + '.py'
        py_file = os.path.join(output_dir, py_file_name)

        def write_file():
            print('Writing ' + py_file)

            with open(py_file, 'w') as f:
                f.write(spec_code)

        if os.path.exists(py_file):
            def do_nothing():
                print('Doing nothing.')

            possible_answers = {
                'Y': write_file,
                'N': do_nothing,
                'A': None
            }
            opts = '/'.join(possible_answers.keys())
            answer = None

            while answer not in possible_answers:
                if got_all:
                    answer = 'Y'
                else:
                    answer = raw_input('Are you sure you want to override file (' +
                        py_file_name + ')?\n' + opts + '\n')
                    answer = answer.upper()

                    if answer == 'A':
                        got_all = True
                        answer = 'Y'

            possible_answers[answer]()
        else:
            write_file()

def run_tests(spec_files):
    if len(spec_files) == 0:
        print('\nNo specifications found!')

        return False
    else:
        print('\nRunning specifications')

        run(spec_files)

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

        time.sleep(1)

def show_version(*args):
    print("speccer %s" % __init__.__version__)
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
        dest="output_folder", type="string",
        callback=output_tests,
        help="output generated test files to given folder")

    options, args = parser.parse_args()

    if len(sys.argv) < 2:
        run_tests(get_specs())
    elif len(args) > 0:
        # TODO: make Python imports work with relative paths in order to enable this
        # expand dir contents to args
        #args = list(chain(*map(lambda a: map(lambda b: os.path.join(a, b), os.listdir(a)) if os.path.isdir(a) else a, args)))

        # get rid of files end with other than .spec or not containing extension at all
        args = filter(lambda a: a.endswith('.spec') or a.find('.') == -1, args)

        # add .spec to files that don't have it yet
        args = map(lambda a: a + '.spec' if not a.endswith('.spec') else a, args)

        # make sure files really exist
        args = filter(lambda a: os.path.exists(a), args)

        run_tests(args)

if __name__ == '__main__':
    main()
