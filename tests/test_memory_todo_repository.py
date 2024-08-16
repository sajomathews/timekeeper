import pytest

from timekeeper.adapters.todos.memory import TodosMemoryCombinedRepository
from timekeeper.domain.todos.interfaces import TodosCompositeRepository, NewTodo, Todo

MISSING_ID = 72

@pytest.fixture
def initial_items() -> list[Todo]:
    return [
        Todo(0, 'title for 0th item'),
        Todo(1, 'title for 1st item', 'some description', parent=0),
        Todo(2, 'subtask', parent=0, percent_complete=1.0, done=True),
        Todo(3, 'subtask', parent=1, percent_complete=1.0, done=True),
        Todo(4, 'subtask', parent=1, percent_complete=0.0)
    ]

@pytest.fixture
def repository(initial_items) -> TodosMemoryCombinedRepository:
    return TodosMemoryCombinedRepository({item.id: item for item in initial_items})

@pytest.fixture
def empty_repository() -> TodosMemoryCombinedRepository:
    return TodosMemoryCombinedRepository({})

@pytest.fixture
def new_todo() -> NewTodo:
    return NewTodo(title="A random new todo", parent=5)


def test_create_todo(empty_repository: TodosCompositeRepository, new_todo: NewTodo):
    item = empty_repository.create(new_todo)
    assert item.id is not None 
    assert item.title == new_todo.title
    assert item.parent == new_todo.parent

def test_create_after_init(repository: TodosMemoryCombinedRepository, new_todo: NewTodo, initial_items: list[Todo]):
    item = repository.create(new_todo)
    assert item.title == new_todo.title
    assert repository.counter == len(initial_items) + 1

def test_read_todo(repository: TodosCompositeRepository, initial_items: list[Todo]):
    item = repository.read(initial_items[0].id)
    assert item == initial_items[0]
    with pytest.raises(Exception):
        item = repository.read(MISSING_ID)

def test_update_todo(repository: TodosCompositeRepository):
    item = repository.read(1)
    item.done = True
    repository.update(item)
    test_item = repository.read(1)
    assert test_item == item
    assert test_item.done == True

def test_mark_children_done(repository: TodosCompositeRepository):
    items = repository.mark_children_done(0)
    assert len(items) == 2 # Children of node 0

def test_update_percent_complete(repository: TodosCompositeRepository):
    item = repository.update_percent_completed(1)
    assert item.percent_complete == 0.5
    item = repository.update_percent_completed(0)
    assert item.percent_complete == 0.75

def test_list(repository: TodosCompositeRepository, initial_items):
    items = repository.list(0, 2)
    assert len(items) == 2
    assert items[0] == initial_items[0]
    items = repository.list(1, 2)
    assert items[0] == initial_items[2]
    items = repository.list(1,3)
    assert items[0] == initial_items[3]
    items = repository.list(5,2)
    assert len(items) == 0
