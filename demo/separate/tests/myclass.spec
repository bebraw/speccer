from demo import myclass

set up
    c = myclass.MyClass()

adds two and two
    c.add(2,2) == 4

adds negatives
    c.add(10, -10) == 0

fails adding int and string
    c.add(10, 'foo') raises TypeError
