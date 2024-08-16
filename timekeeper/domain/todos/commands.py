from dataclasses import dataclass
from timekeeper.domain.todos.interfaces import *

@dataclass
class TodosCommands:
    repository: TodosCompositeRepository

    def create(self, title: str) -> Todo:
        return self.repository.create(NewTodo(title=title))
    
    def create_subtask(self, parent_id: TodoIDType, title: str) -> tuple[Todo, list[Todo]]:
        item = self.repository.create(NewTodo(title, parent=parent_id))
        updates = self.update_percent_completed_all(parent_id)
        return item, updates
    
    def mark_as_done(self, id: TodoIDType) -> list[Todo]:
        item = self.repository.read(id)
        item.done = True
        item.percent_complete = 1.0 
        self.repository.update(item)
        
        items = [item]

        items.extend(self.update_percent_completed_all(item.parent))
        items.extend(self.mark_children_done(id))
        return items
    
    def mark_as_not_done(self, id: TodoIDType) -> list[Todo]:
        item = self.repository.read(id)
        item.done = False
        self.repository.update(item)
        items = []

        items.extend(self.update_percent_completed_all(item.id))
        return items

    def update_percent_completed(self, id: TodoIDType) -> Todo:
        item = self.repository.read(id)
        if item.done:
            return item
        return self.repository.update_percent_completed(id)
    
    def update_percent_completed_all(self, id: TodoIDType) -> list[Todo]:
        items = []
        parent_id = id
        while(parent_id != ROOT):
            parent = self.update_percent_completed(parent_id)
            items.append(parent)
            parent_id = parent.parent

        return items

    
    def mark_children_done(self, id: TodoIDType) -> list[Todo]:
        items = []
        children = self.repository.mark_children_done(id)
        items.extend(children)
        for child in children:
            items.extend(self.mark_children_done(child.id))
        return items
    
    def delete_task(self, id: TodoIDType) -> list[Todo]:
        parent_id = self.repository.read(id).parent
        self.repository.delete(id)
        d = self.repository.delete_orphans()
        print(d)
        updates = self.update_percent_completed_all(parent_id)
        return updates
    
    def update(self, id: TodoIDType, title: str, description: str) -> Todo:
        item = self.repository.read(id)
        item.description = description
        item.title = title
        return self.repository.update(item)
        
            