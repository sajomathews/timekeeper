from dataclasses import dataclass
from typing import Protocol, TypeAlias, List

DEFAULT_ITEMS_PER_PAGE = 10
TodoIDType: TypeAlias = int
ROOT = -1

@dataclass
class Todo:
    id: TodoIDType 
    title: str 
    description: str | None = None 
    parent: TodoIDType  = ROOT 
    done: bool = False 
    percent_complete: float = 0.0

@dataclass
class NewTodo:
    title: str
    description: str | None = None 
    parent: TodoIDType = ROOT
    done: bool = False 
    percent_complete: float = 0.0


class TodosReadRepository(Protocol):
    def list(self, page: int, items_per_page: int = DEFAULT_ITEMS_PER_PAGE, parent: TodoIDType|None = None) -> list[Todo]:
        ...

    def read(self, id: TodoIDType) -> Todo:
        ... 

class TodosWriteRepository(Protocol):
    def create(self, item: NewTodo) -> Todo:
        ...

    def update(self, item: Todo) -> Todo:
        ...
    
    def delete(self, id: TodoIDType) -> None:
        ...

    def mark_children_done(self, id: TodoIDType) -> list[Todo]:
        ...

    def update_percent_completed(self, id: TodoIDType) -> Todo:
        ...

    def delete_orphans(self) -> List[Todo]:
        ...


class TodosCompositeRepository(TodosReadRepository, TodosWriteRepository, Protocol):
    pass

class TodosCombinedRepository(TodosCompositeRepository):
    def __init__(self, reader: TodosReadRepository, writer: TodosWriteRepository):
        self.reader = reader
        self.writer = writer

    def list(self, page: int, items_per_page: int = DEFAULT_ITEMS_PER_PAGE, parent: TodoIDType | None = None) -> List[Todo]:
        return self.reader.list(page, items_per_page)
    
    def read(self, id: TodoIDType) -> Todo:
        return self.reader.read(id)
    
    def create(self, item: NewTodo) -> Todo:
        return self.writer.create(item)
    
    def update(self, item: Todo) -> None:
        self.writer.update(item)
    
    def delete(self, id: TodoIDType) -> None:
        self.writer.update(id)

    def mark_children_done(self, id: int) -> List[Todo]:
        return self.writer.mark_children_done(id)
    
    def update_percent_completed(self, id: int) -> Todo:
        return self.writer.update_percent_completed(id)
    
    def delete_orphans(self) -> List[Todo]:
        return self.writer.delete_orphans()
