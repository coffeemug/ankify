# Tanki
An efficient command line/terminal interface to add cards to Anki

![Screencast](https://raw.githubusercontent.com/coffeemug/tanki/master/cast.gif "Screencast")

# Usage

- Ctrl-t - toggle mode (`->` is a one way card, `<->` two way card, `[ ]` cloze deletion)
- Ctrl-d - drop the current card and start from scratch
- Ctrl-u - sync with the server
- Ctrl-c - quit

# Caveat

Currently the program depends on note types that don't exist in Anki
proper (I cloned some in Anki to have a nicer layour). You can reverse
engineer the fields from the code (see `concept.py`, `jeopardy.py`,
and `quote.py`).

I plan to add code that does this setup, but for now, sorry!