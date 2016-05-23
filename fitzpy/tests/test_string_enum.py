from fitzpy.string_enum import StringEnum, Str, Prop
from nose.tools import ok_, eq_

label1 = 'On Update'
help1 = 'This will be transactional'
label2 = 'On delete'
help2 = 'This will be a soft delete'

class EventTypes(StringEnum):
    on_update = Str()
    on_create = Str()
    on_delete = Str()

class EventStr(Str):
    label = Prop()
    help_text = Prop()
    
class CustomizedEventTypes(StringEnum):
    on_update = EventStr(label=label1, help_text=help1)
    on_delete = EventStr(label=label2, help_text=help2)

def test_basic_string_enum():
    eq_('on_update', EventTypes.on_update)
    eq_('on_create', EventTypes.on_create)
    eq_(3, len(EventTypes.get_values()))
    ok_(EventTypes.has_key('on_update'))
    ok_(not EventTypes.has_key('_all_fields'))
    ok_(not EventTypes.has_key('jabberwocky'))
    
def test_customized_string_enum():
    
    eq_('on_update', CustomizedEventTypes.on_update)
    eq_('on_delete', CustomizedEventTypes.on_delete)
    eq_(label1, CustomizedEventTypes.on_update.label)
    eq_(label2, CustomizedEventTypes.on_delete.label)



        
        

