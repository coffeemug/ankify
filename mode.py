
from jeopardy import Jeopardy
from concept import Concept
from quote import Quote
import sync as s

card_types = [Jeopardy, Concept, Quote]
current_mode = 0
syncing = False

def init(x):
    s.init(x)
    anki_current = x.models.current()['name']
    for idx, card_type in enumerate(card_types):
        if anki_current in card_type.anki_note_types():
            current_mode = idx
            return

def toggle():
    global current_mode
    current_mode += 1
    if current_mode >= len(card_types):
        current_mode = 0

def current():
    if syncing:
        return 'syn'
    return card_types[current_mode].name()

def card():
    return card_types[current_mode]()

def sync():
    global syncing
    syncing = True
    try:
        s.synchronize()
    finally:
        syncing = False
