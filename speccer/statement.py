# -*- coding: utf-8 -*-
from functools import partial
from string import strip
from utils import OrderedDict


def _convert(split_char, assertion, line):
    parts = map(strip, line.split(split_char))
    ret = ''

    for l, r in zip(parts, parts[1:]):
        l = l.strip('=').strip()
        op = assertion
 
        if r.startswith('='):
            op += 'Equal'
            r = r.strip('=').strip()

        ret += 'self.assert' + op + '(' + l + ', ' + r + ');'

    return ret

def convert(line):
    s = OrderedDict([
        ('==', 'Equal'),
        ('!=', 'NotEqual'),
        ('!~=', 'NotAlmostEqual'),
        ('~=', 'AlmostEqual'),
        (lambda line: bool(line.count('>') > 1), partial(_convert, '>', 'Greater')),
        (lambda line: bool(line.count('<') > 1), partial(_convert, '<', 'Less')),
        ('>=', 'GreaterEqual'),
        ('<=', 'LessEqual'),
        ('>', 'Greater'),
        ('<', 'Less'),
        ('raises', lambda line: ['try:' + line.split('raises')[0], 'except' + line.split('raises')[1] + ': pass']),
        (' is not instanceof ', 'NotIsInstance'),
        (' is instanceof ', 'IsInstance'),
        ('for ', lambda line: line),
        (' not in ', 'NotIn'),
        (' in ', 'In'),
        (' is not None', 'IsNotNone'),
        (' is None', 'IsNone'),
        (' is not ', 'IsNot'),
        (' is ', 'Is'),
    ])

    def to_lambda(i):
        def to_code(k, v, line):
            l, op, r = line.rpartition(k)
            params = ', '.join(map(strip, (l, r))).rstrip().rstrip(',')

            return 'self.assert' + v + '(' + params + ')'

        k, v = i
        new_v = v if callable(v) else partial(to_code, k, v)

        del s[k]

        if callable(k):
            s[k] = new_v
        else:
            s[lambda line: k in line] = new_v
    
    map(to_lambda, s.items())
    matches = filter(lambda k: k(line), s.keys())
    return s[matches[0]](line) if len(matches) else line

