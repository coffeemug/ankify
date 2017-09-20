
from ui import *

class Jeopardy:
    def __init__(self):
        self.a = None
        self.q = None
        self.details = None
    
    def input(self):
        self.a = uinput(text='Answer:', required=True, example="Leo Tolstoy's year of birth")
        self.q = uinput(text='Question:', required=True, example='What is 1828')
        self.details = uinput(text='Pronunciation/mnemonics?', example='tall-stoi')

    def output(self):
        print_accent('\n*** Card ***')
        print(self.a)
        print_hr()
        print(self.q)
        if self.details:
            print_hr()
            print(self.details)
        print()

    def save(self, x):
        if self.details:
            m = x.models.byName('Basic+details')
        else:
            m = x.models.byName('Basic')
        x.decks.current()['mid'] = m['id']
        n = x.newNote()
        n['Front'] = self.a
        n['Back'] = self.q
        if self.details:
            n['Details'] = self.details
        x.addNote(n)
        x.save()
        print_loud('Card saved!', nl=2)

    @staticmethod
    def anki_note_types():
        return ['Basic', 'Basic+details']

    @staticmethod
    def name():
        return '->'

