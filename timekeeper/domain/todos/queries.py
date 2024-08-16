from dataclasses import dataclass
from timekeeper.domain.todos.interfaces import TodosReadRepository, TodoIDType, Todo, ROOT

DEFAULT_ITEMS_PER_PAGE = 10
FIRST_PAGE = 0

@dataclass
class TodoQueryEngine:
    repository: TodosReadRepository

    def get(self, id: TodoIDType) -> Todo:
        return self.repository.read(id)
    
    def getRoots(self, page: int = FIRST_PAGE, items_per_page: int = DEFAULT_ITEMS_PER_PAGE) -> list[Todo]:
        return self.repository.list(page, items_per_page, parent=ROOT)
    
    def getRootsCount(self, page:int = FIRST_PAGE, items_per_page: int = DEFAULT_ITEMS_PER_PAGE) -> int:
        return len(self.repository.list(page, items_per_page, parent=ROOT))
    
    def getChildren(self, id: TodoIDType, page: int = FIRST_PAGE, items_per_page: int = DEFAULT_ITEMS_PER_PAGE) -> list[Todo]:
        return self.repository.list(page, items_per_page, parent=id)
    
    def getChildrenCount(self, id: TodoIDType, page: int = FIRST_PAGE, items_per_page: int = DEFAULT_ITEMS_PER_PAGE) -> int:
        return len(self.repository.list(page, items_per_page, parent=id))
    