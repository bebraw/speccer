from speccer import processor

def prefix():
    return 8 * ' '

def process(c, line):
    return c.process_line('    ' + line)

set up
    c = processor.SpecificationProcessor('processor')

skips def
    c.process_line('def foo():') == 'def foo():'

skips return
    c.process_line(prefix() + 'return True') == prefix() + 'return True'

processes declaration
    c.process_line('process this  ') == '\n    ' + 'def test_process_this(self):'

chomps apostrophe
    c.process_line("can't touch this") == '\n    ' + 'def test_cant_touch_this(self):'

processes indentation
    process(c, 'a = 5') == prefix() + 'a = 5'

processes equals
    process(c, 'b == 10') == prefix() + 'self.assertEqual(b, 10)'

processes not equals
    process(c, 'b != 10') == prefix() + 'self.assertNotEqual(b, 10)'

processes almost equals
    process(c, 'b ~= 10') == prefix() + 'self.assertAlmostEqual(b, 10)'

processes not almost equals
    process(c, 'b !~= 10') == prefix() + 'self.assertNotAlmostEqual(b, 10)'

processes greater than
    process(c, 'b > 5') == prefix() + 'self.assertGreater(b, 5)'

processes greater than or equals
    process(c, 'b >= 5') == prefix() + 'self.assertGreaterEqual(b, 5)'

processes less than
    process(c, 'b < 5') == prefix() + 'self.assertLess(b, 5)'

processes less than or equals
    process(c, 'b <= 5') == prefix() + 'self.assertLessEqual(b, 5)'

processes multiple lesser inequalities
    process(c, '4 < b <= 10') == prefix() + 'self.assertLess(4, b);self.assertLessEqual(b, 10);'

processes multiple greater inequalities
    process(c, '4 >= b > 10') == prefix() + 'self.assertGreaterEqual(4, b);self.assertGreater(b, 10);'

processes in
    process(c, 'a in [1, 2, 3]') == prefix() + 'self.assertIn(a, [1, 2, 3])'

processes not in
    process(c, 'a not in [1, 2, 3]') == prefix() + 'self.assertNotIn(a, [1, 2, 3])'

skips for in
    process(c, 'for i in a:') == prefix() + 'for i in a:'

processes is
    process(c, 'a is b') == prefix() + 'self.assertIs(a, b)'

processes is not
    process(c, 'a is not b') == prefix() + 'self.assertIsNot(a, b)'

processes is None
    process(c, 'a is None') == prefix() + 'self.assertIsNone(a)'

processes is not None
    process(c, 'a is not None') == prefix() + 'self.assertIsNotNone(a)'

processes is instance
    process(c, 'a is instanceof b') == prefix() + 'self.assertIsInstance(a, b)'

processes is not instance
    process(c, 'a is not instanceof b') == prefix() + 'self.assertNotIsInstance(a, b)'

processes empty line
    process(c, '    ') == ''

processes newline
    process(c, '\n') == ''

processes comment
    c.process_line('# my comment') == '# my comment'
    c.process_line('    # my comment') == '    # my comment'

processes raises
    process(c, 'a raises TypeError') == prefix() + 'with self.assertRaises(TypeError):\n' + prefix() + '    a'

processes anything
    c.process_line('some test') == '\n    def test_some_test(self):'
    c.process_line('foobar') == '    foobar'
    c.process_line('') == ''
    c.process_line('other test') == '\n    def test_other_test(self):'
    c.process_line('') == ''
    c.process_line('yet another test') == '\n    def test_yet_another_test(self):'

processes comma
    c.process_line("some, some") == '\n    def test_some__some(self):'

processes comment at beginning
    c.process_line('#some comment') == '#some comment'
    c.process_line('') == ''
