from speccer import processor

set up
    c = processor.SpecificationProcessor('processor')

processes empty lines
    c.process(['', '']) == ''

