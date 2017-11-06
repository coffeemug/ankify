
from jeopardy import Jeopardy
from concept import Concept
from quote import Quote
from prompt_toolkit.keys import Keys
import sync as s
import ui

card_types = [Concept, Jeopardy, Quote]
current_mode = 0
current_card = None

def init(x):
    s.init(x)
    ui.add_key(Keys.ControlT, toggle)
    ui.add_key(Keys.ControlU, sync)

def toggle(e):
    global current_mode
    current_mode += 1
    cleanup_card()
    set_current_card(None)
    if current_mode >= len(card_types):
        current_mode = 0
    e.cli.exit()

def sync(e):
    e.cli.exit()
    s.synchronize()

def make_card():
    cleanup_card()
    set_current_card(card_types[current_mode]())
    return current_card

def cleanup_card():
    if current_card and ('cleanup' in dir(current_card)):
        current_card.cleanup()

def set_current_card(val):
    global current_card
    current_card = val
    if val:
        ui.mode_name = current_card.name()
        
