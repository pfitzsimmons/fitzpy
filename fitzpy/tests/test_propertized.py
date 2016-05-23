from datetime import datetime
from nose.tools import eq_, ok_
from fitzpy.propertized import Prop, Propertized

class Book(Propertized):
    author = Prop(default='', help_text='Who wrote the book')
    title = Prop(default='')
    publisher = Prop()
    sold_count = Prop(default=0)
    categories = Prop(default=list)
    created_at = Prop(default=lambda:datetime.utcnow())
    isbn = Prop(mutable=False)
    
def test_book():
    author = "Mark Twain"
    book = Book(author="Mark Twain")
    # Default to zero
    eq_(0, book.sold_count)
    eq_('', book.title)
    eq_(author, book.author)
    print 'CATS ', book.categories
    book.categories.append('fiction')
    eq_(['fiction'], book.categories)
    ok_(book.created_at.year > 2000)
    eq_(None, book.publisher)

    d = book.as_dict()
    eq_(author, d['author'])
    prop = [prop for prop in book.list_class_props() if prop.attr_name == 'author'][0]
    eq_('Who wrote the book', prop.help_text)
    
    
def test_immutable():
    isbn = "11133"
    raised = False
    try:
        book = Book(isbn=isbn)
        book.isbn = 'newisbn'
    except AttributeError:
        raised = True
    ok_(raised)

def test_attribute_error():
    raised = False
    try:
        book = Book(titttle='A Tale of Two Cities')
    except AttributeError:
        raised = True
    ok_(raised)
    
