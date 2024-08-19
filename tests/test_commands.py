import pytest
from pathlib import Path
import tempfile

from timekeeper.adapters.todos.sqllite import TodosSQLiteRepository
from timekeeper.domain.todos.commands import TodosCommands

@pytest.fixture
def empty_repository():
    tmp_db_path = tempfile.mktemp()
    yield TodosSQLiteRepository(Path(tmp_db_path))
    Path(tmp_db_path).unlink()

@pytest.fixture
def commander(empty_repository):
    return TodosCommands(empty_repository)

def test_create_command(commander):
    item = commander.create('A new task')
    assert item.id is not None 
    assert item.id == 1
    assert commander.repository.read(item.id).title == item.title 

def test_create_subtask(commander):
    parent = commander.create('Parent')
    child, _ = commander.create_subtask(parent.id, "Child")
    assert child.id is not None 
    assert child.parent == parent.id 

def test_mark_as_done(commander):
    t1 = commander.create('T1')
    t2, _ = commander.create_subtask(t1.id, 'T2')
    t3, _= commander.create_subtask(t1.id, 'T3')
    t4, _ = commander.create_subtask(t2.id, 'T4')
    commander.mark_as_done(t2.id)
    test = commander.repository.read(t2.id)
    assert test.id == t2.id
    assert test.done == True
    assert test.percent_complete == 1.0
    subtask = commander.repository.read(t4.id)
    assert subtask.id == t4.id
    assert subtask.done == True
    assert subtask.percent_complete == 1.0 
    parent = commander.repository.read(t1.id)
    assert parent.done == False 
    assert parent.percent_complete == 0.5

