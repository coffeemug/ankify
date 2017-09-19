
from ui import *

class Jeopardy:
    def __init__(self):
        self.term = None
        self.defin = None
        self.details = None
    
    def input(self):
        self.defin = uinput(text='Answer:', required=True,
                            example='A tax on activity with negative externalities')
        self.term = uinput(text='Question:', required=True, example='What is Pigouvian tax?')
        self.details = uinput(text='Pronunciation/mnemonics?', example='pig-oo-vian')

    def output(self):
        print_accent('\n*** Card ***')
        print(self.term)
        print_hr()
        print(self.defin)
        if self.details:
            print_hr()
            print(self.details)
        print()

    def save(self, x):
        if self.details:
            m = x.models.byName('Basic/reversed+details')
        else:
            m = x.models.byName('Basic (and reversed card)')
        x.decks.current()['mid'] = m['id']
        n = x.newNote()
        n['Front'] = self.term
        n['Back'] = self.defin
        if self.details:
            n['Details'] = self.details
        x.addNote(n)
        x.save()
        print_loud('Card saved!', nl=2)

