import inspect

class Prop(property):
    attr_name = None
    
    def __init__(self, default=None, mutable=True, help_text='', **kwargs):
        self.default = default
        self.mutable = mutable
        self.help_text = help_text
        self.__dict__.update(kwargs)

    def __get__(self, instance=None, owner=None):
        if not self.attr_name:
            raise ValueError('self.attr_name is empty')
        self._check_set_default(instance)
        return instance.__dict__.get(self.attr_name)

    def _check_set_default(self, instance):
        if self.attr_name in instance.__dict__:
            return
        if self.default != None:
            if inspect.isfunction(self.default) or inspect.ismethod(self.default) or inspect.isfunction(self.default):
                instance.__dict__[self.attr_name] = self.default()
            elif isinstance(self.default, type):
                instance.__dict__[self.attr_name] = self.default()
            else:
                instance.__dict__[self.attr_name] = self.default
            self.__set__(instance, instance.__dict__[self.attr_name])

    def __set__(self, instance=None, value=None):
        if not self.mutable and self.attr_name in instance.__dict__:
            raise AttributeError("Property " + self.attr_name + " is immutable and cannot be changed once set.")
        instance.__dict__[self.attr_name] = value

class PropertizedMetaClass(type):
    def __new__(meta, name, bases, atts):
        typ = super(PropertizedMetaClass, meta).__new__(meta, name, bases, atts)
        _class_props = []
        for key, value in atts.items():
            if isinstance(value, Prop):
                value.attr_name = key
                _class_props.append(value)
        typ._class_props = _class_props
        return typ

    
class Propertized(object):
    __metaclass__ = PropertizedMetaClass

    def __init__(self, **kwargs):
        self._hydrate_from_kwargs(**kwargs)

    def as_dict(self):
        d = {}
        for prop in self.list_class_props():
            d[prop.attr_name] = getattr(self, prop.attr_name)
        return d

    @classmethod
    def list_class_props(cls):
        return cls._class_props
            

    def _hydrate_from_kwargs(self, **kwargs):
        prop_names = [prop.attr_name for prop in self.list_class_props()]
        for key, val in kwargs.items():
            if key not in prop_names:
                raise AttributeError("Class " + self.__class__.__name__ + " does not have the property " + key)
            setattr(self, key, val)
        
    
