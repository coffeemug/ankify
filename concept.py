
import ui
from ui import *
from prompt_toolkit.keys import Keys

is_concept_handle = True
def toggle_concept_handle(e):
    global is_concept_handle
    is_concept_handle = not is_concept_handle
    e.cli.exit()

class Concept:
    def __init__(self):
        self.concept = None
        self.desc = None
        self.details = None
        ui.add_key(Keys.ControlH, toggle_concept_handle)

    def cleanup(self):
        ui.drop_key(toggle_concept_handle)
    
    def input(self):
        self.concept = uinput(text='Concept:', required=True, example='Pigouvian tax')
        self.desc = uinput(text='Description:', required=True,
                            example='A tax on negative externalities')
        if is_concept_handle:
            self.desc = "<b>[concept handle]</b> " + self.desc
        self.details = uinput(text='Pronunciation/mnemonics?', example='pig-oo-vian')

    def output(self):
        print_accent('\n*** Card ***')
        print(self.concept)
        print_hr()
        print(self.desc)
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
        n['Back'] = self.desc
        if self.details:
            n['Details'] = self.details
        x.addNote(n)
        x.save()
        print_loud('Card saved!', nl=2)

    def name(self):
        if is_concept_handle:
            return '<h>'
        else:
            return '<->'

