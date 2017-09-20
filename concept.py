
from ui import *

class Concept:
    def __init__(self):
        self.concept = None
        self.defin = None
        self.details = None
    
    def input(self):
        self.concept = uinput(text='Concept:', required=True, example='Pigouvian tax')
        self.defin = uinput(text='Definition:', required=True,
                            example='A tax on activity with negative externalities')
        self.details = uinput(text='Pronunciation/mnemonics?', example='pig-oo-vian')

    def output(self):
        print_accent('\n*** Card ***')
        print(self.concept)
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
        n['Front'] = self.concept
        n['Back'] = self.defin
        if self.details:
            n['Details'] = self.details
        x.addNote(n)
        x.save()
        print_loud('Card saved!', nl=2)

    @staticmethod
    def anki_note_types():
        return ['Basic (and reversed card)', 'Basic/reversed+details']

