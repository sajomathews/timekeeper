from dataclasses import dataclass

from fasthtml.ft import *
from timekeeper.config import Page
from timekeeper.components import icons

@dataclass 
class MenuItem:
    id: int
    label: str
    target_id: str
    href: str = '#'
    active: bool = False

    def render(self):
        return Li(
            AX(
                f'{self.label}', 
                hx_get=self.href,
                target_id=self.target_id, 
                hx_swap="outerHTML",
                cls = 'active m-1' if self.active else 'm-1'
            )
        )
    
@dataclass
class NavBar:
    menu_items: dict[Page, MenuItem]
    active_page: int

    def render(self):
        self.set_active()
        return (Nav(cls="navbar max-w-7xl px-4 lg:px-8 mx-auto bg-base-100")(
                    mobile_menu(self.menu_items.values()),
                    desktop_menu(self.menu_items.values()), 
                    Label(cls='swap swap-rotate')(
                        Input(type='checkbox', cls='theme-controller', value='light'),                       
                        icons.Sun(cls='swap-on h-7 w-7 fill-current'),
                        icons.Moon(cls='swap-off h-7 w-7 fill-current'),
                    )        
                ), 
        )
    
    def set_active(self):
        for item in self.menu_items.values():
            item.active = False 
        self.menu_items[self.active_page].active = True

def desktop_menu(menu_items: list[MenuItem]):
    return Div(cls='navbar-start hidden lg:flex')(
        Ul(cls='menu menu-horizontal px-1')(
            *[item.render() for item in menu_items]
        )
    )
        

def mobile_menu(menu_items: list[MenuItem]):
    return Div(cls='navbar-start')(
        Div(cls='dropdown')(
            Div(tabindex=0, role='button', cls='btn btn-ghost lg:hidden')(
                icons.Menu()
            ),
            Ul(tabindex=0, cls='menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow')(
                *[item.render() for item in menu_items]
            )
        ),
        icons.Logo(),
        H1('Timekeeper', cls='leading-tight font-bold text-2xl')
    )
