import pytest
from pathlib import Path
import tempfile

from timekeeper.adapters.todos.sqllite import TodosSQLiteRepository
from timekeeper.domain.todos.interfaces import NewTodo, Todo

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
def empty_repository():
    tmp_db_path = tempfile.mktemp()
    yield TodosSQLiteRepository(Path(tmp_db_path))
    Path(tmp_db_path).unlink()

@pytest.fixture
def repository(empty_repository, initial_items):
    for item in initial_items:
        empty_repository.db.t.todos.insert(item)
    return empty_repository

@pytest.fixture
def new_todo() -> NewTodo:
    return NewTodo(title="A random new todo", parent=5)


def test_create_todo(empty_repository, new_todo: NewTodo):
    item = empty_repository.create(new_todo)
    assert item.id is not None 
    assert item.title == new_todo.title
    assert item.parent == new_todo.parent

def test_create_todo_post_init(repository, new_todo):
    item = repository.create(new_todo)
    assert item.id is not None
    assert item.title == new_todo.title

def test_update_todo(repository, initial_items):
    item = initial_items[0]
    item.done = True
    repository.update(item)
    test_item = Todo(**repository.db.t.todos()[0])
    assert test_item == item
    assert test_item.done == True

def test_mark_children_done(repository):
    items = repository.mark_children_done(0)
    assert len(items) == 2 # Children of node 0
    assert items[0].id == 1

def test_update_percent_complete(repository):
    item = repository.update_percent_completed(1)
    assert item.percent_complete == 0.5
    item = repository.update_percent_completed(0)
    assert item.percent_complete == 0.75

def test_list(repository, initial_items):
    items = repository.list(0, 2)
    assert len(items) == 2
    assert items[0] == initial_items[0]
    items = repository.list(1, 2)
    assert items[0] == initial_items[2]
    items = repository.list(1,3)
    assert items[0] == initial_items[3]
    items = repository.list(5,2)
    assert len(items) == 0

def test_read(repository, initial_items):
    item = repository.read(2)
    assert item == initial_items[2]

def test_read_todo(repository, initial_items):
    item = repository.read(initial_items[0].id)
    assert item == initial_items[0]
    with pytest.raises(Exception):
        item = repository.read(MISSING_ID)