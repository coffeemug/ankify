# Ankify
An efficient command line/terminal interface to add cards to Anki

![Screencast](https://raw.githubusercontent.com/coffeemug/ankify/master/cast.gif "Screencast")

# Usage

- `Ctrl-t` - toggle mode (`->` is a one way card, `<->` two way card, `[ ]` cloze deletion)
- `Ctrl-d` - drop the current card and start from scratch
- `Ctrl-u` - sync with the server
- `Ctrl-c` - quit

When in `<->` (two way) mode:
- `Ctrl-h` to pick the handle type. This adds a label to the fields (e.g. `[concept handle]`, `[word]`, or no label)

When on `Pronunciation/mnemonics` steps:
- `Ctrl-i` to enter image search mode. This mode integrates with google images to quickly find images for mnemonics to add them to the card. Requires iTerm (for images support in the terminal).
- When done with image mode, hit `Ctrl-i` again.

# Caveat

Currently the program depends on note types that don't exist in Anki
proper (I cloned some in Anki to have a nicer layout). You can reverse
engineer the fields from the code (see `concept.py`, `jeopardy.py`,
and `quote.py`).

I plan to add code that does this setup, but for now, sorry!
