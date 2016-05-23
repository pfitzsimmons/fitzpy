import sys

def import_thing(name):
    '''
    Imports a class, function, object, module or whatever from a string path
    '''
    components = name.split('.')
    path = components[0]
    last_part = None
    thing = __import__(path)
    try:
        for part in components[1:]:
            path = path + '.' + part            
            if hasattr(thing, part):
                thing = getattr(thing, part)
                continue
            thing = __import__(path)
            for path_part in path.split('.')[1:]:
                thing = getattr(thing, path_part)
    except ImportError:
        sys.stderr.write('Error importing %s' % name)
        raise
    except AttributeError:
        sys.stderr.write('Error importing %s' % name)
        raise
    if thing == None:
         raise ValueError('Mysterious error calling import_thing("%s"): imported thing is None' % name)
    return thing
    

