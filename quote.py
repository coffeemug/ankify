
from ui import *
import re

class Quote:
    def __init__(self):
        self.quote = None
        self.author = None
        self.source = None
        self.extra = None


    def input(self):
        self.quote = uinput(text='Quote:', required=True,
                            example="You can't build [a peaceful world] on [empty stomachs]")
        self.author = uinput(text='Author:', required=True, example='Norman Borloug')
        self.source = uinput(text='Source:', required=True, example='Penn Jillette interview')
        self.extra = uinput(text='Pronunciation/mnemonics?', example='north man bore log')

    def output(self):
        print_accent('\n*** Card ***')
        print(self.quote)
        print('  - [' + self.author + '] via [' + self.source + ']')
        if self.extra:
            print_hr()
            print(self.extra)
        print()

    def save(self, x):
        if self.extra:
            m = x.models.byName('Cloze+details')
        else:
            m = x.models.byName('Cloze')
        x.decks.current()['mid'] = m['id']
        n = x.newNote()
        i = 0
        n['Text'] = self.to_anki()
        if self.extra:
            n['Extra'] = self.extra
        x.addNote(n)
        x.save()
        print_loud('Card saved!', nl=2)

    def to_anki(self):
        i = 0
        def rfn(m):
            nonlocal i
            i += 1
            return '{{c' + str(i) + '::'
        text = re.sub('\\[', rfn, self.quote)
        text = re.sub('\\]', '}}', text)
        text += '<br><br>'
        text += '- {{c' + str(i+1) + '::' + self.author + '}}'
        text += ' via '
        text += '{{c' + str(i+2) + '::' + self.source + '}}'
        return text
        
