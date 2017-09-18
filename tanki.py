
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

# prompt_toolkit helpers
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
    Token.Title: '#2980b9',
    Token.Hr: '#884444',
})

# UI elements helpers
def make_toolbar(txt):
    exit_msg = 'Ctrl-c/d'
    if txt:
        return lambda _: [(Token.Toolbar, '(e.g. ' + txt + ') | ' + exit_msg)]
    else:
        return lambda _: [(Token.Toolbar, exit_msg)]

def uinput(text=None, required=False, example=None, uprompt=None):
    if text:
        print_tokens([(Token.Label, text + '\n')], style=style)
    promptl = [(Token.Label, uprompt)] if uprompt else []
    promptl.append((Token, '> '))
    return prompt(get_prompt_tokens=lambda _: promptl,
                  style=style,
                  validator = Required() if required else None,
                  get_bottom_toolbar_tokens=make_toolbar(example))

def print_hr():
    print_tokens([(Token.Hr, '---\n')], style=style)

def print_dropped_msg():
    print_tokens([(Token.Dropped, 'Card dropped!\n\n')], style=style)

# Card I/O helpers
def input_card():
    term = uinput(text='Enter question:', required=True, example='What is Pigouvian tax?')
    defin = uinput(text='Answer:', required=True,
                   example='A tax on activity with negative externalities')
    details = uinput(text='Pronunciation/mnemonics?', example='pig-oo-vian')
    return (term, defin, details)

def print_card(card):
    (term, defin, details) = card
    print_tokens([(Token.Title, '\n*** Card ***\n')], style=style)
    print(term)
    print_hr()
    print(defin)
    if details:
        print_hr()
        print(details)
    print()

def savep(card):
    while True:
        should = uinput(uprompt='Save card? (Y\\n)')
        if not should or should == 'Y' or should == 'y':
            return True
        elif should == 'N' or should == 'n':
            print_dropped_msg()
            return False

# Anki interaction code
def save_card(card, x):
    (term, defin, details) = card
    if details:
        m = x.models.byName('Basic/reversed+details')
    else:
        m = x.models.byName('Basic (and reversed card)')
    x.decks.current()['mid'] = m['id']
    n = x.newNote()
    n['Front'] = term
    n['Back'] = defin
    if details:
        n['Details'] = details
    x.addNote(n)
    x.save()
    print_tokens([(Token.Saved, 'Card saved!\n\n')], style=style)

# Main loop...
def main():
    x = aopen(db_path)
    while True:
        try:
            card = input_card()
            print_card(card)
            if savep(card):
                save_card(card, x)
        except EOFError:
            print_dropped_msg()
        except KeyboardInterrupt:
            x.close()
            sys.exit()

def usage():
    print("Usage: {}\n  add cards to Anki".format(sys.argv[0]))

if __name__ != '__main__' or len(sys.argv) > 1:
    usage()
    sys.exit()

main()
