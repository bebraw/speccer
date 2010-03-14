set up
    c = myclass.MyClass() # this has to match to module name

adds two and two
    c.add(2,2) == 4

adds negatives
    c.add(10, -10) == 0

#this_fails
#    c.foobar()

fails adding int and string
    c.add(10, 'foo') raises TypeError
