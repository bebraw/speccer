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
    process(c, '    ') == None

processes comment
    process(c, '# some comment') == None
    process(c, '    # some comment') == None

processes raises
    process(c, 'a raises TypeError') == prefix() + 'try:a \n        except TypeError: pass'
