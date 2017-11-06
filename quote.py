
from ui import *
import re

class Quote:
    def __init__(self):
        self.quote = None
        self.source = None
        self.extra = None

    def input(self):
        self.quote = uinput(text='Quote:', required=True,
                            example="Life is [suffering]")
        self.source = uinput(text='Source:', example='[Buddha] via [Pali Canon]')
        self.extra = uinput(text='Pronunciation/mnemonics?', example='pah-lee')

    def output(self):
        print_accent('\n*** Card ***')
        print(self.quote)
        if self.source:
            print('  - ' + self.source)
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
        n['Text'] = self._to_anki()
        if self.extra:
            n['Extra'] = self.extra
        x.addNote(n)
        x.save()
        print_loud('Card saved!', nl=2)

    def name(self):
        return '[ ]'

    def _to_anki(self):
        i = 0
        def rfn(m):
            nonlocal i
            i += 1
            return '{{c' + str(i) + '::'
        text = self.quote
        if self.source:
            text += '<br><br>- ' + self.source
        text = re.sub('\\[', rfn, text)
        text = re.sub('\\]', '}}', text)
        return text
        
