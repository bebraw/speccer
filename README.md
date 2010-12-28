## Speccer - Specification based test runner for Python

Run "setup.py install" to start rocking. See "demo" folder for an actual example. Once you have installed the tool just invoke "speccer" at that directory. You should see some test results. Feel free to tweak the files to give it a proper go.

## Basic Specification Syntax

As you probably didn't bother checking demo folder or so let's take a look at a concrete example:

myclass.spec: (tests myclass.py)

    set up
        c = myclass.MyClass()

    adds two and two
        c.add(2,2) == 4

    adds negatives
        c.add(10, -10) == 0

    fails adding int and string
        c.add(10, 'foo') raises TypeError

It looks pretty much like any other test you may have seen before. The syntax may be a bit lighter, though.

"set up" is a predefined test method that is run before each specification. This way you can set up some objects ie. like in this case.

Each specification contains a name and some actual code asserting something. I have listed available assertions below:

* ==, is equal
* !=, is not equal
* ~=, is almost equal
* !~=, is not almost equal
* \>, bigger than
* \>=, bigger than or equal
* <, smaller than
* <=, smaller than or equal
* x < y < z, multiple inequalities (mix with equality as you want)

These assertions map directly to ones available in Python's unittest module. If some of those seem weird to you, see http://docs.python.org/library/unittest.html .
