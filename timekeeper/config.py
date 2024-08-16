from enum import IntEnum, StrEnum

class Page(IntEnum):
    DASHBOARD = 1
    WORK_ITEMS = 2
    TEAM = 3
    NOTES = 4
    HABITS = 5

class Routes(StrEnum):
    DASHBOARD = '/'
    WORK_ITEMS = '/work'
    WORK_ITEM = '/work/{id}'
    WORK_ITEM_COMPLETED = '/work/{id}/completed'
    TEAM = '/team'
    NOTES = '/notes'
    HABITS = '/habits'
