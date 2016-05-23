import inspect
from fitzpy.importing import import_thing
from nose.tools import ok_, eq_


def test_import_module():
    d1 = import_thing('datetime')
    ok_(hasattr(d1, 'datetime'))
    d2 = import_thing('datetime.datetime')
    ok_(inspect.isclass(d2))
    d3 = import_thing('datetime.datetime.utcnow')
    is_func = inspect.isfunction(d3)
    ok_(d3)




