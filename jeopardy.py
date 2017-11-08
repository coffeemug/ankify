
from ui import *

class Jeopardy:
    def __init__(self):
        self.desc = None
        self.fact = None
        self.details = None
    
    def input(self):
        self.desc = uinput(text='Description:', required=True, example="Tolstoy's year of birth")
        self.fact = uinput(text='Fact:', required=True, example='1828')
        self.details = uinput(text='Pronunciation/mnemonics?', example='tall-stoi',
                              allow_images=True)

    def output(self):
        print_accent('\n*** Card ***')
        print(self.desc)
        print_hr()
        print(self.fact)
        if self.details:
            print_hr()
            print(self.details)
        summarize_images()
        print()

    def save(self, x):
        m = x.models.byName('Basic+details')
        x.decks.current()['mid'] = m['id']
        n = x.newNote()
        n['Front'] = self.desc
        n['Back'] = self.fact
        
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
        return '->'

