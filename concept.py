
import ui
import random
from ui import *
from prompt_toolkit.keys import Keys

label_chain = ['c', 'w', 'b', None]

def label():
    return label_chain[0]

def toggle_concept_handle(e):
    global label_chain
    label_chain = label_chain[1:] + label_chain[:1]
    ui.mode_name = fmt_card_mode()

def fmt_card_mode():
    return {
        'c' : '<c>',
        'w' : '<w>',
        'b' : '<b>',
        None : '<->',
    }[label()]

def fmt_label(txt):
    return {
        'c' : '<b>[concept]</b> ',
        'w' : '<b>[word]</b> ',
        'b' : '<b>[bio]</b> ',
        None : '',
    }[label()] + txt
    
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
        # randomize order (since the concept headline and definition
        # are interchangable/makes two cards, shuffling makes learning
        # easier)
        self.concept, self.desc = random.sample([self.concept, self.desc], 2)

        # Add the label
        self.concept = fmt_label(self.concept)
        self.desc = fmt_label(self.desc)

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
