
import sys
import os.path
import mode
from ui import *
import config
from anki import Collection as aopen

# Main loop...
def main():
    config.init()
    x = aopen(config.db_path())
    mode.init(x)
    while True:
        try:
            card = mode.card()
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
