from dataclasses import dataclass, field

from timekeeper.domain.todos.interfaces import *
from timekeeper.domain.todos.interfaces import NewTodo, Todo, TodoIDType 

THRESHOLD = 1e-4

@dataclass
class TodosMemoryCombinedRepository(TodosCompositeRepository):
    items: dict[int, Todo]
    counter: int = field(init=False)

    def __post_init__(self):
        self.counter = len(self.items)


    def create(self, item: NewTodo) -> Todo:
        t = Todo(id=self.counter, title=item.title, parent=item.parent)
        self.items[self.counter] = t 
        self.counter += 1
        return t
    
    def update(self, item: Todo) -> None:
        self.items[item.id] = item

    def delete(self, id: int) -> None:
        del self.items[id]

    def mark_children_done(self, id: TodoIDType) -> list[Todo]:
        items = [item for item in self.items.values() if item.parent == id]
        for item in items: 
            item.done = True
            item.percent_complete = 1.0
        return items
    
    def update_percent_completed(self, id: TodoIDType) -> Todo:
        items = [item for item in self.items.values() if item.parent == id]
        self.items[id].percent_complete = sum((item.percent_complete for item in items) ) / len(items)
        if abs(self.items[id].percent_complete - 1.0) < THRESHOLD:
            self.items[id].done = True

        return self.items[id]
    
    def list(self, page: TodoIDType, items_per_page: TodoIDType = ...) -> list[Todo]:
        count = len(self.items)
        offset = page * items_per_page

        items = list(self.items.values())[offset:offset + items_per_page]
        return items
    
    def read(self, id: TodoIDType) -> Todo:
        return self.items[id]