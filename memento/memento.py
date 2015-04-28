"""
memento pattern:

Reference:
1)https://github.com/faif/python-patterns/blob/master/memento.py
2)http://code.activestate.com/recipes/413838-memento-closure/
"""

import copy


def memento(obj, deep=False):
    state = (copy.copy, copy.deepcopy)[bool(deep)](obj.__dict__)

    def restore():
        obj.__dict__.clear()
        obj.__dict__.update(state)
    return restore


class Transaction:

    """A transaction guard. This is really just
      syntactic suggar arount a memento closure.
      """
    deep = False

    def __init__(self, *targets):
        self.targets = targets
        self.commit()

    def commit(self):
        self.states = [memento(target, self.deep) for target in self.targets]

    def rollback(self):
        for st in self.states:
            st()


class Transactional(object):

    """Adds transactional semantics to methods. Methods decorated  with
    @transactional will rollback to entry state upon exceptions.
    """

    def __init__(self, method):
        self.method = method

    def __get__(self, obj, T):
        def transaction(*args, **kwargs):
            state = memento(obj)
            try:
                return self.method(obj, *args, **kwargs)
            except:
                state()
                raise
        return transaction


class NumObj(object):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<%s: %r>' % (self.__class__.__name__, self.value)

    def increment(self):
        self.value += 1

    @Transactional
    def do_stuff(self):
        self.value = '1111'  # <- invalid value
        self.increment()     # <- will fail and rollback


if __name__ == '__main__':
    n = NumObj(-1)
    print(n)
    t = Transaction(n)
    try:
        for i in range(3):
            n.increment()
            print(n)
        t.commit()
        print('-- commited')
        for i in range(3):
            n.increment()
            print(n)
        n.value += 'x'  # will fail
        print(n)
    except:
        t.rollback()
        print('-- rolled back')
    print(n)
    print('-- now doing stuff ...')
    try:
        n.do_stuff()
    except:
        print('-> doing stuff failed!')
        import sys
        import traceback
        traceback.print_exc(file=sys.stdout)
        pass
    print(n)

"""
OUTPUT:
<NumObj: -1>
<NumObj: 0>
<NumObj: 1>
<NumObj: 2>
-- commited
<NumObj: 3>
<NumObj: 4>
<NumObj: 5>
-- rolled back
<NumObj: 2>
-- now doing stuff ...
-> doing stuff failed!
Traceback (most recent call last):
  File "G:\Github\design-patterns-in-action\memento\momento.py", line 98, in <module>
    n.do_stuff()
  File "G:\Github\design-patterns-in-action\memento\momento.py", line 53, in transaction
    return self.method(obj, *args, **kwargs)
  File "G:\Github\design-patterns-in-action\memento\momento.py", line 74, in do_stuff
    self.increment()     # <- will fail and rollback
  File "G:\Github\design-patterns-in-action\memento\momento.py", line 69, in increment
    self.value += 1
TypeError: Can't convert 'int' object to str implicitly
<NumObj: 2>
"""