import os
from speccer import processor

def process(c, filename):
    def read(prefix):
        return open(os.path.join('testcases', prefix + '_' + filename + '.py')).read().split('\n')

    given = read('given')
    trunk = read('expected')
    trunk.pop()

    expected = ['...'] * 4
    expected.extend(trunk)
    expected.extend(['...'] * 2)

    result = c.process(given).split('\n')

    tests = [(a, b) for a, b in zip(expected, result) if a != b and a != '...']

    if len(tests):
        print '\n' + str(tests) + '\n'

set up
    c = processor.SpecificationProcessor('processor')

processes empty lines
    c.process(['', '']) == ''

processes function
    process(c, 'function')

processes function and test
    process(c, 'function_and_test')

processes test
    process(c, 'test')

processes hoisting
    process(c, 'hoisting')

# TODO: test assignment!
# TODO: test long str at beginning of a func!

