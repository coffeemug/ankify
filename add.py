
import sys
import re
import os.path
from anki import Collection as aopen
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.contrib.completers import WordCompleter
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
    return (lambda cli: [(Token.Toolbar, '(e.g. ' + txt + ') or Ctrl-c/d')]) if txt else None

def uinput(txt, required=False, example=None, complete=None):
    print_tokens([(Token.Label, txt + '\n')], style=style)
    return prompt('> ', style=style,
                  validator = Required() if required else None,
                  get_bottom_toolbar_tokens=make_toolbar(example),
                  completer=WordCompleter(complete) if complete else None)

def input_card(x):
    term = uinput('Enter term:', required=True, example='Pigouvian tax')
    pronun = re.sub(r'^\(|\)$', '', uinput('Pronunciation?', example='pig-oo-vian'))
    defin = uinput('Definition:', required=True,
                   example='A tax levied on any market activity with negative externalities')
    details = uinput('Extra details?', example='Invented by Cambridge economist Arthur Pigou')
    tags = uinput('Tags?', example=' '.join(x.tags.all()), complete=x.tags.all())
    return (term, pronun, defin, details, tags)

def parenify(x):
    return "({})".format(x)

def print_card(card):
    (term, pronun, defin, details, tags) = card
    print_tokens([(Token.Card, '\n*** Card ***\n')], style=style)
    print(term)
    if pronun:
        print(parenify(pronun))
    print('---\n' + defin)
    if details:
        print('---\n' + details)
    if tags:
        print('---\nTags: ' + tags)
    print()

def save_card(card, x):
    (term, pronun, defin, details, tags) = card
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
    if tags:
        n.setTagsFromStr(tags)
    x.addNote(n)
    x.save()
    print_tokens([(Token.Saved, 'Card saved!\n\n')], style=style)

def savep(card):
    while True:
        should = prompt(get_prompt_tokens=lambda _: [(Token.Label, 'Save card? (Y\\n)'),
                                                     (Token, '> ')],
                       style=style)
        if not should or should == 'Y' or should == 'y':
            return True
        elif should == 'N' or should == 'n':
            print_tokens([(Token.Dropped, 'Card dropped!\n\n')], style=style)
            return False

def main():
    x = aopen(db_path)
    while True:
        try:
            card = input_card(x)
            print_card(card)
            if savep(card):
                save_card(card, x)
        except EOFError:
            print()
        except KeyboardInterrupt:
            x.close()
            sys.exit()

if __name__ != '__main__' or len(sys.argv) > 1:
    usage()
    sys.exit()

main()
