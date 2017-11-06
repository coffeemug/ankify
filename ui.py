
from prompt_toolkit.key_binding.manager import KeyBindingManager
from pygments.token import Token
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt

# what mode are we in (for the toolbar)
mode_name = ""
key_bindings = {}

# key bindings interface
manager = KeyBindingManager.for_prompt()

def add_key(key, callback):
    key_bindings[callback] = key
    manager.registry.add_binding(key)(callback)

def drop_key(callback):
    key_bindings.pop(callback, None)
    manager.registry.remove_binding(callback)

# uinput is kinda big
def uinput(text=None, required=False, example=None, uprompt=None, password=False):
    if text:
        print_tokens([(Token.Label, text + '\n')], style=style)
    promptl = [(Token.Label, uprompt)] if uprompt else []
    promptl.append((Token, '> '))
    return prompt(get_prompt_tokens=lambda _: promptl,
                  style=style,
                  validator = Required() if required else None,
                  get_bottom_toolbar_tokens=make_toolbar(example, mode_name),
                  key_bindings_registry=manager.registry,
                  is_password=password)

class Required(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message='Required', cursor_position=0)

def make_toolbar(txt, mode):
    toolbar = mode.rjust(4)
    if txt:
        toolbar += ' | :(' + txt + ')'
    toolbar += ' | Ctrl-d/c/' + format_bindings()
    return lambda _: [(Token.Toolbar, toolbar)]

def format_bindings():
    keys = []
    for key in key_bindings.values():
        name = key.name.replace("<", "").replace(">", "")
        keys.append(name[-1])
    return "/".join(keys).lower()

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

