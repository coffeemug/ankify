
import ui
from ui import *
from prompt_toolkit.keys import Keys

is_concept_handle = True
def toggle_concept_handle(e):
    global is_concept_handle
    is_concept_handle = not is_concept_handle
    ui.mode_name = fmt_card_mode()

def fmt_card_mode():
    if is_concept_handle:
        return '<h>'
    else:
        return '<->'
    
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
        self.details = uinput(text='Pronunciation/mnemonics?', example='pig-oo-vian',
                              allow_images=True)
        if is_concept_handle:
            self.desc = "<b>[concept handle]</b> " + self.desc

    def output(self):
        print_accent('\n*** Card ***')
        print(self.concept)
        print_hr()
        print(self.desc)
        if self.details:
            print_hr()
            print(self.details)
        summarize_images()
        print()

    def save(self, x):
        m = x.models.byName('Basic/reversed+details')
        x.decks.current()['mid'] = m['id']
        n = x.newNote()
        n['Front'] = self.concept
        n['Back'] = self.desc

        combined_details = ''
        html = ui.images_save_htmlify(x)
        if html:
            combined_details += html
        if self.details:
            combined_details += self.details
        if combined_details != '':
            n['Details'] = combined_details
            
        x.addNote(n)
        x.save()
        print_loud('Card saved!', nl=2)

    def name(self):
        return fmt_card_mode()
