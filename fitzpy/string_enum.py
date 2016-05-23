'''
StringEnum is a replacement for using a class of Constants as an enum.

Original:

class Events(object):
  on_update = 'on_update'
  on_create = 'on_create'

The above is bad, beause it easy to have a naming bug where the String value does not match the attribute.

So instead we do this:

class Events(StringEnum):
  on_update = Str()
  on_create = Str()

The metaclass introspects the class definition and replaces the Str() attribute value with
the string value.

Thus:
>print Events.on_update
"on_update"
> isinstance(Events.on_update, str)
True

This means it is easy to serialize the value, store it in the database, or do other string-like things with it.

For instance, we can use it in a SQL Alchemy Column definition:

my_column = db.Column(db.Enum(Events.get_values()))

If we want to get really fancy, we can add metadata to the Enum value:

class MyVal(Str):
  label = Prop()
  help_text = Prop()

class Events(StringEnum):
  on_update = MyVal(label='On Update', help_text='This event happens after the object is updated')

>assert Events.on_update == 'on_update'
>assert Events.on_update.label == 'On Update'

'''

from fitzpy.propertized import Propertized, Prop

class StrWrapper(str):
    def __new__(cls, s, **kwargs):
        newobj = str.__new__(cls, s)
        for key, value in kwargs.items():
            setattr(newobj, key, value)
        return newobj

class Str(Propertized):
    pass

class StringEnumMeta(type):
    def __new__(meta, name, bases, atts):
        _all_fields = []
        for key, val in atts.items():
            if isinstance(val, Str):
                new_val = StrWrapper(key, **val.as_dict())
                atts[key] = new_val
                _all_fields.append(new_val)
        atts['_all_fields'] = _all_fields
        typ = super(StringEnumMeta, meta).__new__(meta, name, bases, atts)
        return typ

class StringEnum(object):
    __metaclass__ = StringEnumMeta

    @classmethod
    def get_values(cls):
        return sorted(cls._all_fields) #pylint:disable=E1101

    @classmethod
    def has_key(cls, key):
        return isinstance(getattr(cls, key, None), StrWrapper)
