
class Todo:
    todo = {}

    def add_todo(self, value):
        self.todo.update({len(self.todo.keys()): {'marked': False, 'value': value}})

    def mark(self, pos):
        self.todo[pos]['marked'] = not self.todo[pos]['marked']

    def values(self):
        return [
            {'id': f'todo_id_{todo_key}', **self.todo[todo_key]}
            for todo_key in self.todo
        ]



def assign_globals(gl):
    for gl_key in gl:
        if gl_key in globals():
            continue
        globals()[gl_key] = gl[gl_key]

def render(values):
    root = Element('root')
    root.clear()
    for value in values:
        root.write(value, append=True)
    for value in values:
        if not hasattr(value, 'bind_actions'):
            continue
        value.bind_actions()

class TodoListItem:
    def __init__(self, id_=None, value="", marked=False, on_click=None):
        self.id = id_
        self.value = value
        self.marked = marked
        self.on_click = on_click
    
    def bind_actions(self):
        Element(self.id).element.onclick = self.on_click

    def _repr_html_(self):
        checked = ""
        if self.marked:
            checked = "checked"
        return f"""
        <div>
            <input type="checkbox" id="{self.id}" {checked}>
            {self.value}
        </div>
        """

def create_todo_list_item(todo, value):
    def on_click(*args, **kwargs):
        todo.mark(int(value['id'].split('_')[-1]))
        render(view_todo(todo))
    return TodoListItem(id_=value['id'], value=value['value'], marked=value['marked'], on_click=on_click)

def create_todo_list(todo):
    return [
        create_todo_list_item(todo, value)
        for value in todo.values()
    ]


class Button:
    def __init__(self, id_=None, name='Button', on_click=None):
        self.id = id_
        self.name = name
        self.on_click = on_click

    def bind_actions(self):
        Element(self.id).element.onclick = self.on_click

    def _repr_html_(self):
        return f"""
        <button id="{self.id}">{self.name}</button>
        """

def create_button(todo):
    def on_click(*args, **kwargs):
        global INPUT_STR
        global CLEAN_INPUT
        todo.add_todo(INPUT_STR)
        if callable(CLEAN_INPUT):
            CLEAN_INPUT()
        render(view_todo(todo))
    return Button(id_='button1', name='add', on_click=on_click)
INPUT_STR = ''
CLEAN_INPUT = None
class Input:
    def __init__(self, id_=None, on_change=None, value=''):
        self.on_change = on_change
        self.id = id_
        self.value = value

    def bind_actions(self):
        Element(self.id).element.oninput = self.on_change

    def _repr_html_(self):
        return f"""
        <input id="{self.id}" type="text" value="{self.value}">
        """
def create_input(todo):
    global CLEAN_INPUT
    def _():
        global INPUT_STR
        INPUT_STR = ''
        render(view_todo(todo))
    CLEAN_INPUT = _

    def on_change(event, **kwargs):
        global INPUT_STR
        INPUT_STR = event.target.value

    global INPUT_STR
    return Input(id_="inp", on_change=on_change, value=INPUT_STR)


def view_todo(todo):
    return [
        *create_todo_list(todo),
        create_input(todo),
        create_button(todo)
    ]


def main(gl):
    assign_globals(gl)
    todo = Todo()
    todo.add_todo('hey')
    todo.add_todo('yey')
    render(view_todo(todo))