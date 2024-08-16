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

    def render(self, mobile:bool = False):
        active_classes = ['border-indigo-500', 'text-gray-900']
        inactive_classes = ['border-transparent', 'text-gray-500', 'hover:border-gray-300', 'hover:bg-gray-50', 'hover:text-gray-700'] 

        mobile_common_cls = 'block border-l-4 py-2 pl-3 pr-4 text-base font-medium'
        desktop_common_cls = 'inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium'

        common_cls = mobile_common_cls if mobile else desktop_common_cls
        classes = ' '.join(active_classes) if self.active else ' '.join(inactive_classes)

        # Use Alpine.js to set the right classes depending on which menu item is active
        js_obj = """
            {{
            "border-indigo-500": active == {id}, 
            "text-gray-900": active == {id}, 
            "border-transparent": active != {id}, 
            "text-gray-500": active != {id}, 
            "hover:border-gray-300": active != {id}, 
            "hover:bg-gray-50": active != {id}, 
            "hover:text-gray-700": active != {id} 
            }}
        """

        return AX(
                f'{self.label}', 
                hx_get=self.href,
                target_id=self.target_id, 
                hx_swap="outerHTML",
                cls=f'{common_cls} {classes}',
                **{':class':js_obj.format(id=self.id), "@click":f"active = {self.id}"}
                )
    
@dataclass
class NavBar:
    menu_items: dict[Page, MenuItem]
    active_page: int

    def render(self):
        self.set_active()
        # Setup an alpine.js component
        return Nav(cls='border-b border-gray-200 bg-white', x_data=f'{{active:{self.active_page}}}')(
            desktop_menu(self.menu_items.values()),
            mobile_menu(self.menu_items.values())    
        )
    
    def set_active(self):
        for item in self.menu_items.values():
            item.active = False 
        self.menu_items[self.active_page].active = True

def desktop_menu(menu_items: list[MenuItem]):
    return Div(cls='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8')(
                Div(cls='flex h-16 justify-between')(
                    Div(cls='flex')(
                        Div(cls='flex flex-shrink-0 items-center')(
                            icons.Logo()
                            #Img(src='https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600', alt='Your Company', cls='block h-8 w-auto lg:hidden'),
                            #Img(src='https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600', alt='Your Company', cls='hidden h-8 w-auto lg:block')
                        ),
                        Div(cls='hidden sm:-my-px sm:ml-6 sm:flex sm:space-x-8')(
                            *[item.render() for item in menu_items]
                            )
                    ),
                )
            )   
        

def mobile_menu(menu_items: list[MenuItem]):
    return Div(id='mobile-menu', cls='sm:hidden')(
                Div(cls='space-y-1 pb-3 pt-2')(
                    *[item.render(mobile=True) for item in menu_items]
                )
            )
