from fasthtml import common as fh
from fasthtml.ft import *
from timekeeper.components.work_items import * 

from timekeeper.adapters.todos.sqllite import TodosSQLiteRepository
from timekeeper.domain.todos.commands import TodosCommands
from timekeeper.domain.todos.queries import TodoQueryEngine
from timekeeper.components.navigation import MenuItem
from timekeeper.components.layout import Layout, MAIN_CONTENT_ID, main_content
from timekeeper.config import Page, Routes
from timekeeper.domain.todos.interfaces import ROOT


# Setup tailwindcss from CDN
tlink = Script(src="https://cdn.tailwindcss.com?plugins=typography")
daisyui = Link(href="https://cdn.jsdelivr.net/npm/daisyui@4.12.10/dist/full.min.css", rel="stylesheet", type="text/css")
alpinejs = Script(defer=True, src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js")

# setup the main application
app = fh.FastHTMLWithLiveReload(hdrs=(alpinejs, daisyui, tlink))

# setup the navigation
MENU = [
    MenuItem(Page.DASHBOARD, 'Dashboard', MAIN_CONTENT_ID, href=Routes.DASHBOARD),
    MenuItem(Page.WORK_ITEMS,'Work Items', MAIN_CONTENT_ID, href=Routes.WORK_ITEMS),
    MenuItem(Page.TEAM,'Team', MAIN_CONTENT_ID, href=Routes.TEAM),
    MenuItem(Page.NOTES,'Notes', MAIN_CONTENT_ID,href=Routes.NOTES),
    MenuItem(Page.HABITS,'Habits', MAIN_CONTENT_ID, href=Routes.HABITS)
]
menu_items = {item.id: item for item in MENU}

# dependency injection
repository = TodosSQLiteRepository('data/timekeeper.db')
commander = TodosCommands(repository)
query_engine = TodoQueryEngine(repository)


# Setup routing

# Home page
@app.get(Routes.DASHBOARD)
def main(htmx):
    title = 'Dashboard'
    if not htmx.request:
        return Layout(title, Page.DASHBOARD, menu_items).render()
    else:
        return main_content(title)

# Work Items
@app.get(Routes.WORK_ITEMS)
def get_work(htmx, page:int = 0):
    title = 'Work Items'
    todo_roots = query_engine.getRoots(page=page)
    count_next = query_engine.getRootsCount(page=page + 1)
    items = work_items(todo_roots, parent=ROOT, count_next_page=count_next, page=page)
    if not htmx.request:
        return Layout(title, Page.WORK_ITEMS, menu_items).render(new_task_input(), items)
    else:
        return main_content(title, new_task_input(), items)
    
@app.post(Routes.WORK_ITEMS)
def add_work(title: str):
    return WorkItem(commander.create(title)).render()

@app.put(Routes.WORK_ITEM)
def update_work(id: int, title: str, description: str):
    item = commander.update(id, title=title, description=description)
    return WorkItem(item).render()

@app.delete(Routes.WORK_ITEM)
def delete_work_item(id: int):
    updates = commander.delete_task(id)
    items = [WorkItem(item).percent_complete(swap=True) for item in updates]
    return tuple(items)

@app.post(Routes.WORK_ITEM)
def add_subtask(id: int, title: str):
    item, updates = commander.create_subtask(parent_id=id, title=title)
    return WorkItem(item).render(), tuple(WorkItem(u).percent_complete(swap=True) for u in updates)

@app.get(Routes.WORK_ITEM)
def get_subtasks(id: int, page: int = 0):
    items = query_engine.getChildren(id, page=page)
    count_next = query_engine.getChildrenCount(id, page=page + 1)
    return work_items(items, count_next_page=count_next, parent=id, page=page)

@app.patch(Routes.WORK_ITEM_COMPLETED)
def mark_completed(id: int, completed: bool):
    updates = commander.mark_as_done(id) if completed else commander.mark_as_not_done(id)
    items = [WorkItem(item).render() if item.id == id else WorkItem(item).percent_complete(swap=True) for item in updates]
    return tuple(items)
        

# Notes
@app.get(Routes.NOTES)
def notes(htmx):
    title = 'Notes'
    if not htmx.request:
        return Layout(title, Page.TEAM, menu_items).render()
    else:
        return main_content(title)
    
# Team
@app.get(Routes.TEAM)
def team(htmx):
    title = 'Team'
    if not htmx.request:
        return Layout(title, Page.TEAM, menu_items).render()
    else:
        return main_content(title)

# Habits 
@app.get(Routes.HABITS)
def habits(htmx):
    title = 'Habits'
    if not htmx.request:
        return Layout(title, Page.HABITS, menu_items).render()
    else:
        return main_content(title)

# Start the server
fh.serve()

