
from jeopardy import Jeopardy
from concept import Concept
from quote import Quote

card_types = [Jeopardy, Concept, Quote]
current_mode = 0

def init(x):
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
    return card_types[current_mode].__name__.lower()

def card():
    return card_types[current_mode]()

