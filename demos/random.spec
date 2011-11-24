# original: http://docs.python.org/library/unittest.html#basic-example
import random

set up
    seq = range(10)

doesn't lose any elements
    random.shuffle(seq)
    seq.sort()

    seq == range(10)

raises exception for an immutable sequence
    random.shuffle((1, 2, 3)) raises TypeError

chooses element in sequence
    random.choice(seq) in seq

raises exception for too high value
    random.sample(seq, 20) raises ValueError

samples from sequence
    for element in random.sample(seq, 5):
        element in seq

