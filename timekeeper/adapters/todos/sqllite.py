from pathlib import Path

from fasthtml import common as fh

from timekeeper.domain.todos.interfaces import *
from timekeeper.domain.todos.interfaces import NewTodo, Todo, TodoIDType 

DEFAULT_ITEMS_PER_PAGE = 10

MARK_CHILDREN_DONE = """
UPDATE TODOS SET DONE=TRUE, PERCENT_COMPLETE=1.0 WHERE PARENT=? RETURNING *
"""

UPDATE_PERCENT_COMPLETE = """
UPDATE TODOS 
SET PERCENT_COMPLETE=
(
    SELECT COALESCE(AVG(COALESCE(PERCENT_COMPLETE,0)),0) FROM TODOS WHERE PARENT=?
) 
WHERE ID=? 
RETURNING *
"""

LIST_TODOS = """
SELECT * FROM TODOS
ORDER BY DONE, PERCENT_COMPLETE DESC
LIMIT ?
OFFSET ?
"""

FILTERED_TODOS = """
SELECT * FROM TODOS
WHERE PARENT = ?
ORDER BY DONE, PERCENT_COMPLETE DESC
LIMIT ?
OFFSET ?
"""

DELETE_ORPHANS = """
delete from todos 
where id in ( 
    select t1.id 
    from todos t1 
        left outer join 
        todos t2 
        on t1.parent = t2.id 
    where 
        t2.id is NULL and 
        t1.parent <> -1
)
returning *
"""



class TodosSQLiteRepository(TodosCompositeRepository):
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db = fh.database(db_path)
        self.todos = self.db.t.todos

        if self.todos not in self.db.t:
            self.todos.create(id=int, title=str, description=str, parent=int, done=bool, percent_complete=float, pk='id')
    
    def create(self, item: NewTodo) -> Todo:
        todo = self.todos.insert(item)
        print(type(todo), todo)
        return Todo(**todo)
        
    def update(self, item: Todo) -> Todo:
        return Todo(**self.todos.update(item))

    def mark_children_done(self, id: int) -> list[Todo]:
        print(id)
        items = self.db.q(MARK_CHILDREN_DONE, (id,))
        print(items)
        return [Todo(**item) for item in items]
    
    def update_percent_completed(self, id: TodoIDType) -> Todo:
        items = self.db.q(UPDATE_PERCENT_COMPLETE, (id,id))
        return Todo(**items[0])
    
    def list(self, page: TodoIDType, items_per_page: TodoIDType = DEFAULT_ITEMS_PER_PAGE, parent: TodoIDType|None = None) -> list[Todo]:
        offset = page * items_per_page
        if parent is None:
            items = self.db.q(LIST_TODOS, (items_per_page, offset))
        else:
            items = self.db.q(FILTERED_TODOS, (parent, items_per_page, offset))
        return [Todo(**item) for item in items]
    
    def read(self, id: TodoIDType) -> Todo:
        return Todo(**self.todos.get(id))
    
    def delete(self, id: TodoIDType) -> None:
        self.todos.delete(id)

    def delete_orphans(self) -> List[Todo]:
        deletes = self.db.q(DELETE_ORPHANS)
        return [Todo(**d) for d in deletes]



