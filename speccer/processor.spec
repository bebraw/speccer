set up
    c = processor.SpecificationProcessor('processor')

skips def
    c.process_line('def foo():') == 'def foo():'

processes declaration
    c.process_line('process this  ') == '\n    def test_process_this(self):'

processes indentation
    c.process_line('    a = 5') == '        a = 5'

processes equals
    c.process_line('    b == 10') == '        self.assertEqual(b, 10)'

processes not equals
    c.process_line('    b != 10') == '        self.assertNotEqual(b, 10)'

processes almost equals
    c.process_line('    b ~= 10') == '        self.assertAlmostEqual(b, 10)'

processes not almost equals
    c.process_line('    b !~= 10') == '        self.assertNotAlmostEqual(b, 10)'

processes bigger than
    c.process_line('    b > 5') == '        self.assertTrue(b > 5)'

processes bigger than or equals
    c.process_line('    b >= 5') == '        self.assertTrue(b >= 5)'

processes smaller than
    c.process_line('    b < 5') == '        self.assertTrue(b < 5)'

processes smaller than or equals
    c.process_line('    b <= 5') == '        self.assertTrue(b <= 5)'

processes multiple inqualities
    c.process_line('    4 < b < 10') == '        self.assertTrue(4 < b < 10)'
    c.process_line('    4 <= b < 10') == '        self.assertTrue(4 <= b < 10)'
    c.process_line('    4 < b <= 10') == '        self.assertTrue(4 < b <= 10)'
    c.process_line('    4 <= b <= 10') == '        self.assertTrue(4 <= b <= 10)'

processes empty line
    c.process_line('    ') == None

processes comment
    c.process_line('# some comment') == None
    c.process_line('    # some comment') == None

processes raises
    c.process_line('    a raises TypeError') == '        try:a \n        except TypeError: pass'
