
import ui
from ui import *
import sys
import os.path
from anki import Collection as aopen
from jeopardy import Jeopardy
from quote import Quote

# Collection directory
db_path = os.path.expanduser('~/Library/Application Support/Anki2/User 1/collection.anki2')

# Mode management
def on_toggle(e):
    if ui.mode == 'quote':
        ui.mode = 'jeopardy'
    else:
        ui.mode = 'quote'
    e.cli.exit()
set_on_toggle(on_toggle)

# Card I/O helpers
def init_mode(x):
    if x.models.current()['name'] == 'Cloze' or x.models.current()['name'] == 'Cloze+details':
        ui.mode = 'quote'
    else:
        ui.mode = 'jeopardy'

def make_card():
    if ui.mode == 'jeopardy':
        return Jeopardy()
    else:
        return Quote()

# Main loop...
def main():
    x = aopen(db_path)
    init_mode(x)
    while True:
        try:
            card = make_card()
            card.input()
            card.output()
            if yes_no_p('Save card?'):
                card.save(x)
            else:
                print_subdued('Card dropped!', nl=2)
        except EOFError:
            print_subdued('Card dropped', nl=2)
        except KeyboardInterrupt:
            x.close()
            sys.exit()

def usage():
    print("Usage: {}\n  add cards to Anki".format(sys.argv[0]))

if __name__ != '__main__' or len(sys.argv) > 1:
    usage()
    sys.exit()

main()
