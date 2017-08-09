from collections import namedtuple

d = namedtuple('d', 'x')
a = d(x=1)

class B(object):
    @classmethod
    def b(cls, obj):
        print obj.x
