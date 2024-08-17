from dataclasses import dataclass
from enum import IntEnum
from fasthtml.ft import * 
from timekeeper.components.navigation import NavBar, MenuItem
from timekeeper.config import Page

MAIN_CONTENT_ID = 'main_content'


@dataclass
class Layout:
    title: str 
    page: Page
    menu_items: dict[Page, MenuItem]

    def render(self, *children, **attributes):
        nav_bar = NavBar(self.menu_items, self.page)
        page = Body(cls='min-h-full bg-base-100')(
            nav_bar.render(),
            main_content(self.title, *children, **attributes)
        )
        return page
    
def main_content(title: str, *children):
    return Div(cls='py-10', id=MAIN_CONTENT_ID)(
            header(title),
            Main(
                Div(cls='mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8')(
                    *children
                )
            )
        )

def header(text: str):
    return Header(
            Div(cls='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8')(
                H1(text, cls='text-3xl font-bold leading-tight tracking-tight text-base-content')
            )
        )

