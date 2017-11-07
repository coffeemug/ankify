
import sys
from prompt_toolkit.key_binding.manager import KeyBindingManager
from pygments.token import Token
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt
from prompt_toolkit.keys import Keys
from getch import getch
import images

# what mode are we in (for the toolbar)
mode_name = ""
key_bindings = {}
staged_images = {}

# key bindings interface
manager = KeyBindingManager.for_prompt()

def add_key(key, callback):
    key_bindings[callback] = key
    manager.registry.add_binding(key)(callback)

def drop_key(callback):
    key_bindings.pop(callback, None)
    manager.registry.remove_binding(callback)

# uinput is kinda big
def uinput(text=None, required=False, example=None, uprompt=None, password=False,
           allow_images=False):
    def _text_fn():
        if text:
            print_tokens([(Token.Label, text + '\n')], style=style)
    if allow_images:
        on_image_search = make_on_image_search(_text_fn, example)
        add_key(Keys.ControlI, on_image_search)
    _text_fn()
    promptl = [(Token.Label, uprompt)] if uprompt else []
    promptl.append((Token, '> '))
    try:
        res = prompt(get_prompt_tokens=lambda _: promptl,
                     style=style,
                     validator = Required() if required else None,
                     get_bottom_toolbar_tokens=make_toolbar(example),
                     key_bindings_registry=manager.registry,
                     is_password=password)
    finally:
        if allow_images:
            drop_key(on_image_search)
    return res

class Required(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message='Required', cursor_position=0)

def make_toolbar(txt):
    def render_toolbar(_):
        toolbar = mode_name.rjust(4)
        if txt:
            toolbar += ' | :(' + txt + ')'
        if len(staged_images) > 0:
            toolbar += "/i:%d" % len(staged_images)
        toolbar += ' | Ctrl-d/c/' + format_bindings()
        return [(Token.Toolbar, toolbar)]
    return render_toolbar

def format_bindings():
    keys = []
    for key in key_bindings.values():
        name = key.name.replace("<", "").replace(">", "")
        keys.append(name[-1])
    return "/".join(keys).lower()

# image search
def make_on_image_search(text_fn, example):
    def _find_images():
        try:
            while True:
                find_image(example)
        except EOFError:
            pass

    def _on_image_search(e):
        _i = e.cli.current_buffer.text
        if _i != '':
            return
        e.cli.run_in_terminal(_find_images)
        e.cli.run_in_terminal(text_fn)

    return _on_image_search

def find_image(example):
    query = uinput(uprompt='image', example=example)
    if query == '':
        return
    print("Finding images for '%s'..." % query)
    imgs = images.query_images(query)
    images.grid_print(imgs)
    res = pick_image()
    if res:
        staged_images[query] = imgs[res -1]
        print("Added image %d (%s)" % (res, query))

def pick_image():
    sys.stdout.write("Image number 1-8 (or 'q') ")
    sys.stdout.flush()
    while True:
        res = getch()
        if res.isdigit():
            res = int(res)
            if res in range(1,9):
                print()
                return int(res)
        else:
            if res == 'q':
                print()
                return None

# other input elements
def yes_no_p(q):
    while True:
        should = uinput(uprompt=q+' (Y\\n)')
        if not should or should == 'Y' or should == 'y':
            return True
        elif should == 'N' or should == 'n':
            return False

def up_down():
    while True:
        dir = uinput(uprompt='Overwrite dir (U\\D)')
        if dir == 'U':
            return 'u'
        elif dir == 'D':
            return 'd'

# UI elements helpers
def print_subdued(txt, nl=1):
    print_tokens([(Token.Subdued, txt + ('\n' * nl))], style=style)
    
def print_accent(txt, nl=1):
    print_tokens([(Token.Accent, txt + ('\n' * nl))], style=style)
    
def print_loud(txt, nl=1):
    print_tokens([(Token.Loud, txt + ('\n' * nl))], style=style)
    
def print_hr():
    print_subdued('---')

# Styles
style = style_from_dict({
    Token.Label: '#44ff44 italic',
    Token.Toolbar: '#ffffff bg:#333333 italic',
    Token.Subdued: '#884444',
    Token.Accent: '#2980b9',
    Token.Loud: '#ff0066',
})

