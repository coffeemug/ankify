
import sys
import re
import os.path
from anki import Collection as aopen
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from pygments.token import Token
from pprint import pprint

# Collection directory
db_path = os.path.expanduser('~/Library/Application Support/Anki2/User 1/collection.anki2')

def usage():
    print("Usage: {}\n  add cards to Anki".format(sys.argv[0]))

class Required(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message='Required', cursor_position=0)

style = style_from_dict({
    Token.Label: '#44ff44 italic',
    Token.Toolbar: '#ffffff bg:#333333 italic',
    Token.Saved: '#ff0066',
    Token.Dropped: '#884444',
    Token.Card: '#2980b9',
    Token.Hr: '#884444',
})

def make_toolbar(txt):
    return (lambda cli: [(Token.Toolbar, '(e.g. ' + txt + ') or Ctrl-c')]) if txt else None

def uinput(txt, required=False, example=None):
    print_tokens([(Token.Label, txt + '\n')], style=style)
    return prompt('> ', style=style,
                  validator = Required() if required else None,
                  get_bottom_toolbar_tokens=make_toolbar(example))

def input_card():
    term = uinput('Enter term:', required=True, example='Pigouvian tax')
    pronun = re.sub(r'^\(|\)$', '', uinput('Pronunciation?', example='pig-oo-vian'))
    defin = uinput('Definition:', required=True,
                   example='A tax levied on any market activity with negative externalities')
    details = uinput('Extra details?', example='Invented by Cambridge economist Arthur Pigou')
    return (term, pronun, defin, details)

def parenify(x):
    return "({})".format(x)

def print_card(card):
    (term, pronun, defin, details) = card
    print_tokens([(Token.Card, '\n*** Card ***\n')], style=style)
    print(term)
    if pronun:
        print(parenify(pronun))
    print('---\n' + defin)
    if details:
        print('---\n' + details)
    print()

def save_card(card):
    (term, pronun, defin, details) = card
    x = aopen(db_path)
    if details:
        m = x.models.byName('Basic/reversed+details')
    else:
        m = x.models.byName('Basic (and reversed card)')
    x.decks.current()['mid'] = m['id']
    n = x.newNote()
    n['Front'] = term + ('<div>{}</div>'.format(parenify(pronun)) if pronun else '')
    n['Back'] = defin
    if details:
        n['Details'] = details
    x.addNote(n)
    x.save()
    x.close()
    print_tokens([(Token.Saved, 'Card saved!\n\n')], style=style)

def maybe_save(card):
    while True:
        savep = prompt(get_prompt_tokens=lambda _: [(Token.Label, 'Save card? (Y\\n)'),
                                                    (Token, '> ')],
                       style=style)
        if not savep or savep == 'Y' or savep == 'y':
            save_card(card)
            return
        elif savep == 'N' or savep == 'n':
            print_tokens([(Token.Dropped, 'Card dropped!\n\n')], style=style)
            return

def main():
    while True:
        try:
            card = input_card()
            print_card(card)
            maybe_save(card)
        except EOFError:
            print()
            pass
        except KeyboardInterrupt:
            sys.exit()

if __name__ != '__main__' or len(sys.argv) > 1:
    usage()
    sys.exit()

main()
