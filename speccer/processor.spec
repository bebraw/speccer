set up
    c = processor.SpecificationProcessor('processor')

# TODO: figure out a nice syntax to disable parts of spec!

# TODO: this should set context and return all declarations in a dict for **kvargs
#processes set up
#    c.process_line('set up') == 'def set_up()'

#processes declaration
#    c.process_line('process this  ') == 'def process_this():'

#processes indentation
#    c.process_line('    a = 5') == '    a = 5'

processes equals assertion
    c.process_line('    b == 10') == '    assert b == 10'

#processes empty line
#    c.process_line('    ') == None

processes comment
    c.process_line('# some comment') == None
    c.process_line('    # some comment') == None

#processes raises
#    c.process_line('    c.add(10, 'foo') raises TypeError') == "    try: c.add(10, 'foo')\n    except TypeError: pass"