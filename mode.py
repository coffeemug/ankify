
from jeopardy import Jeopardy
from concept import Concept
from quote import Quote
import sync as s

card_types = [Concept, Jeopardy, Quote]
current_mode = 0
current_card = None
syncing = False

def init(x):
    s.init(x)

def toggle():
    global current_mode, current_card
    current_mode += 1
    current_card = None
    if current_mode >= len(card_types):
        current_mode = 0

def name():
    if syncing:
        return 'syn'
    return card().name()

def card():
    global current_card
    if not current_card:
        current_card = card_types[current_mode]()
    return current_card

def sync():
    global syncing
    syncing = True
    try:
        s.synchronize()
    finally:
        syncing = False
