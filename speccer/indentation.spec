renders indentation
    i = indentation.Indentation('    foobar')
    i() == '    '

fails on number
    i = indentation.Indentation(3) raises TypeError
