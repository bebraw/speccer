def prefix():
    return 8 * ' '

def process(c, line):
    return c.process_line('    ' + line)

function = ['def foo():', "    a = 4", "    return 'foo'"]

set up
    c = processor.SpecificationProcessor('processor')

processes empty lines
    c.process(['', '']) == ''

# TODO
#processes function with return
#    c.process(function) == "def foo():\n    a = 4\n    return 'foo'"

skips def
    c.process_line('def foo():') == 'def foo():'

skips return
    c.process_line(prefix() + 'return True') == prefix() + 'return True'

processes declaration
    c.process_line('process this  ') == '\n    ' + 'def test_process_this(self):'

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

processes bigger than
    process(c, 'b > 5') == prefix() + 'self.assertTrue(b > 5)'

processes bigger than or equals
    process(c, 'b >= 5') == prefix() + 'self.assertTrue(b >= 5)'

processes smaller than
    process(c, 'b < 5') == prefix() + 'self.assertTrue(b < 5)'

processes smaller than or equals
    process(c, 'b <= 5') == prefix() + 'self.assertTrue(b <= 5)'

processes multiple inqualities
    process(c, '4 < b < 10') == prefix() + 'self.assertTrue(4 < b < 10)'
    process(c, '4 <= b < 10') == prefix() + 'self.assertTrue(4 <= b < 10)'
    process(c, '4 < b <= 10') == prefix() + 'self.assertTrue(4 < b <= 10)'
    process(c, '4 <= b <= 10') == prefix() + 'self.assertTrue(4 <= b <= 10)'

processes empty line
    process(c, '    ') == ''

processes newline
    process(c, '\n') == ''

processes comment
    c.process_line('# my comment') == '# my comment'
    c.process_line('    # my comment') == '    # my comment'

processes raises
    process(c, 'a raises TypeError') == prefix() + 'try:a \n        except TypeError: pass'

processes anything
    c.process_line('some test') == '\n    def test_some_test(self):'
    c.process_line('foobar') == '    foobar'
    c.process_line('') == ''
    c.process_line('other test') == '\n    def test_other_test(self):'
    c.process_line('') == ''
    c.process_line('yet another test') == '\n    def test_yet_another_test(self):'

processes test with Python
    c.process_line('some test') == '\n    def test_some_test(self):'
    c.process_line('    if True:') == '        if True:'
    c.process_line("        print('works')") == "            print('works')"
    c.process_line('') == ''
    c.process_line("    print('end')") == "        print('end')"

processes long string
    c.process_line('some test') == '\n    def test_some_test(self):'
    c.process_line("    expected = '''") == "        expected = '''"
    c.process_line('var a = 4;') == 'var a = 4;'
    c.process_line('var b = 5;') == 'var b = 5;'
    c.process_line("'''") == "'''"
    c.process_line('') == ''
    c.process_line("    print('done')") == "        print('done')"

processes comment at beginning
    c.process_line('#some comment') == '#some comment'
    c.process_line('') == ''
