from dataclasses import dataclass

from fasthtml.ft import *

from timekeeper.components.custom_ft import *
from timekeeper.domain.todos.interfaces import Todo
from timekeeper.config import Routes
from timekeeper.components import icons
from timekeeper.domain.todos.interfaces import ROOT


@dataclass
class WorkItem:
    item: Todo
    
    @property
    def base_id(self):
        return f'work-item-{self.item.id}'

    def render(self):
        return self.li(
            self.flex_row(self.data(), self.edit_form(), self.action_buttons(),**{'@mouseenter': 'visible=true', '@mouseleave': 'visible=false'}),
            self.subtasks()
        )

    def li(self, *children):

        return Li(
            cls='flex flex-col items-center justify-between gap-y-6 py-2', 
            id=self.base_id,
            x_data = '{visible: false, edit_mode: false, subtasks: false}',
            )(
                Div(cls='w-full overflow-hidden rounded-lg bg-white shadow')(
                    Div(cls='px-2 py-2 sm:p-2')(
                        *children
                    )       
                )
            )
    
    def flex_row(self, *children, **attributes):
        return Div(cls='w-full flex flex-row items-center justify-between gap-x-6 py-1', **attributes)(*children)
    
    def flex_col(self, *children):
        return Div(cls='w-full flex flex-col justify-between gap=y-6 px-5')(*children)
    
    def card(self, header, *children):
        return Div(cls='w-full ml-10 divide-y divide-gray-200 overflow-hidden rounded-lg bg-white shadow', x_show='subtasks')(
            Div(cls='px-4 py-5 sm:px-6')(
                header,
            ),
            Div(cls='px-4 py-5 sm:p-6')(
                *children
            )
        )
    
    def data(self):
        id = f'{self.base_id}-completed'
        vals = '{"completed": "false"}' if self.item.done else '{"completed": "true"}'

        return Div(cls='min-w-0')(
            Div(cls='flex items-start gap-x-3 py-1', x_show='!edit_mode')(
                Div(cls='flex h-6 items-center')(
                    Input(
                        id=id, 
                        aria_describedby='work item completed', 
                        name='completed', 
                        type='checkbox', 
                        checked = True if self.item.done else False,
                        cls='h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600',
                        hx_patch=Routes.WORK_ITEM_COMPLETED.format(id=self.item.id),
                        target_id=self.base_id,
                        hx_swap='outerHTML',
                        hx_vals = vals
                    )
                ),
                Div(cls='ml-3 text-sm leading-6')(
                    Label(
                        fr=id, 
                        cls='font-medium font-semibold leading-6 text-gray-900'
                    )(
                        self.item.title, 
                        self.percent_complete(),
                    ),
                    P(self.item.description, cls='text-gray-500')
                ),
            ),
            # Div(cls='mt-1 flex items-center gap-x-2 text-xs leading-5 text-gray-500')(
            #     P(cls='whitespace-nowrap')(item.description),
            #     Svg(viewbox='0 0 2 2', cls='h-0.5 w-0.5 fill-current')(
            #         Circle(cx='1', cy='1', r='1')
            #     ),
            #     P(f"{item.percent_complete*100:0.1f}%", cls=cls),
            #     Svg(viewbox='0 0 2 2', cls='h-0.5 w-0.5 fill-current')(
            #         Circle(cx='1', cy='1', r='1')
            #     ),
            #     P(f"{item.parent}"),
            #     # P(, cls='truncate')
            # )
        )
    
    def percent_complete(self, swap:bool=False):
        classes_in_progress = 'bg-gray-50 text-gray-600 ring-gray-500/10'
        classes_completed = 'bg-green-50 text-green-700 ring-green-600/20'
        classes_common = 'mt-0.5 whitespace-nowrap rounded-md px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset ml-2.5'
        cls = f"{classes_common} {classes_completed}" if self.item.percent_complete >= 0.5 else f"{classes_common} {classes_in_progress}"
        swap_value = 'true' if swap else None
        return Span(f"{self.item.percent_complete*100:0.1f}%", cls=cls, id=f'{self.base_id}-percent-complete',hx_swap_oob=swap_value)
        
    def edit_form(self):
        id_base = self.base_id
        return Div(cls='min-w-0 w-full', x_show='edit_mode')(
            Form(action='#', cls='relative')(
                Div(cls='overflow-hidden rounded-lg border border-gray-300 shadow-sm focus-within:border-indigo-500 focus-within:ring-1 focus-within:ring-indigo-500')(
                    Label('Title', fr=f'{id_base}-title', cls='sr-only'),
                    Input(type='text', name='title', id=f'{id_base}-title', value=self.item.title, placeholder='Title', cls='block w-full border-0 pt-2.5 text-lg font-medium placeholder:text-gray-400 focus:ring-0'),
                    Label('Description', fr=f'{id_base}-description', cls='sr-only'),
                    Textarea(rows='2', name='description', id=f'{id_base}-description', placeholder='Write a description...', cls='block w-full resize-none border-0 py-0 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6')(
                        self.item.description
                    ),
                    Div(aria_hidden='true')(
                        Div(cls='py-2')(
                            Div(cls='h-9')
                        ),
                        Div(cls='h-px'),
                        Div(cls='py-2')(
                            Div(cls='py-px')(
                                Div(cls='h-9')
                            )
                        )
                    )
                ),
                Div(cls='absolute inset-x-px bottom-0')(
                    # Div(cls='flex flex-nowrap justify-end space-x-2 px-2 py-2 sm:px-3')(
                    #     Div(cls='flex-shrink-0')(
                    #         Label('Assign', id='listbox-label', cls='sr-only'),
                    #         Div(cls='relative')(
                    #             Button(type='button', aria_haspopup='listbox', aria_expanded='true', aria_labelledby='listbox-label', cls='relative inline-flex items-center whitespace-nowrap rounded-full bg-gray-50 px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 sm:px-3')(
                    #                 Svg(viewbox='0 0 20 20', fill='currentColor', aria_hidden='true', cls='h-5 w-5 flex-shrink-0 text-gray-300 sm:-ml-1')(
                    #                     Path(fill_rule='evenodd', d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-5.5-2.5a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zM10 12a5.99 5.99 0 00-4.793 2.39A6.483 6.483 0 0010 16.5a6.483 6.483 0 004.793-2.11A5.99 5.99 0 0010 12z', clip_rule='evenodd')
                    #                 ),
                    #                 Img(src='https://images.unsplash.com/photo-1491528323818-fdd1faba62cc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80', alt='', cls='h-5 w-5 flex-shrink-0 rounded-full'),
                    #                 Span('Assign', cls='hidden truncate sm:ml-2 sm:block')
                    #             ),
                    #             Ul(tabindex='-1', role='listbox', aria_labelledby='listbox-label', aria_activedescendant='listbox-option-0', cls='absolute right-0 z-10 mt-1 max-h-56 w-52 overflow-auto rounded-lg bg-white py-3 text-base shadow ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm')(
                    #                 Li(id='listbox-option-0', role='option', cls='relative cursor-default select-none bg-white px-3 py-2')(
                    #                     Div(cls='flex items-center')(
                    #                         Svg(viewbox='0 0 20 20', fill='currentColor', aria_hidden='true', cls='h-5 w-5 flex-shrink-0 text-gray-400')(
                    #                             Path(fill_rule='evenodd', d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-5.5-2.5a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zM10 12a5.99 5.99 0 00-4.793 2.39A6.483 6.483 0 0010 16.5a6.483 6.483 0 004.793-2.11A5.99 5.99 0 0010 12z', clip_rule='evenodd')
                    #                         ),
                    #                         Span('Unassigned', cls='ml-3 block truncate font-medium')
                    #                     )
                    #                 ),
                    #                 Li(id='listbox-option-1', role='option', cls='relative cursor-default select-none bg-white px-3 py-2')(
                    #                     Div(cls='flex items-center')(
                    #                         Img(src='https://images.unsplash.com/photo-1491528323818-fdd1faba62cc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80', alt='', cls='h-5 w-5 flex-shrink-0 rounded-full'),
                    #                         Span('Wade Cooper', cls='ml-3 block truncate font-medium')
                    #                     )
                    #                 )
                    #             )
                    #         )
                    #     ),
                    #     Div(cls='flex-shrink-0')(
                    #         Label('Add a label', id='listbox-label', cls='sr-only'),
                    #         Div(cls='relative')(
                    #             Button(type='button', aria_haspopup='listbox', aria_expanded='true', aria_labelledby='listbox-label', cls='relative inline-flex items-center whitespace-nowrap rounded-full bg-gray-50 px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 sm:px-3')(
                    #                 Svg(viewbox='0 0 20 20', fill='currentColor', aria_hidden='true', cls='h-5 w-5 flex-shrink-0 text-gray-300 sm:-ml-1')(
                    #                     Path(fill_rule='evenodd', d='M5.5 3A2.5 2.5 0 003 5.5v2.879a2.5 2.5 0 00.732 1.767l6.5 6.5a2.5 2.5 0 003.536 0l2.878-2.878a2.5 2.5 0 000-3.536l-6.5-6.5A2.5 2.5 0 008.38 3H5.5zM6 7a1 1 0 100-2 1 1 0 000 2z', clip_rule='evenodd')
                    #                 ),
                    #                 Span('Label', cls='hidden truncate sm:ml-2 sm:block')
                    #             ),
                    #             Ul(tabindex='-1', role='listbox', aria_labelledby='listbox-label', aria_activedescendant='listbox-option-0', cls='absolute right-0 z-10 mt-1 max-h-56 w-52 overflow-auto rounded-lg bg-white py-3 text-base shadow ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm')(
                    #                 Li(id='listbox-option-0', role='option', cls='relative cursor-default select-none bg-white px-3 py-2')(
                    #                     Div(cls='flex items-center')(
                    #                         Span('Unlabelled', cls='block truncate font-medium')
                    #                     )
                    #                 ),
                    #                 Li(id='listbox-option-1', role='option', cls='relative cursor-default select-none bg-white px-3 py-2')(
                    #                     Div(cls='flex items-center')(
                    #                         Span('Engineering', cls='block truncate font-medium')
                    #                     )
                    #                 )
                    #             )
                    #         )
                    #     ),
                    #     Div(cls='flex-shrink-0')(
                    #         Label('Add a due date', id='listbox-label', cls='sr-only'),
                    #         Div(cls='relative')(
                    #             Button(type='button', aria_haspopup='listbox', aria_expanded='true', aria_labelledby='listbox-label', cls='relative inline-flex items-center whitespace-nowrap rounded-full bg-gray-50 px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 sm:px-3')(
                    #                 Svg(viewbox='0 0 20 20', fill='currentColor', aria_hidden='true', cls='h-5 w-5 flex-shrink-0 text-gray-300 sm:-ml-1')(
                    #                     Path(fill_rule='evenodd', d='M5.75 2a.75.75 0 01.75.75V4h7V2.75a.75.75 0 011.5 0V4h.25A2.75 2.75 0 0118 6.75v8.5A2.75 2.75 0 0115.25 18H4.75A2.75 2.75 0 012 15.25v-8.5A2.75 2.75 0 014.75 4H5V2.75A.75.75 0 015.75 2zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75z', clip_rule='evenodd')
                    #                 ),
                    #                 Span('Due date', cls='hidden truncate sm:ml-2 sm:block')
                    #             ),
                    #             Ul(tabindex='-1', role='listbox', aria_labelledby='listbox-label', aria_activedescendant='listbox-option-0', cls='absolute right-0 z-10 mt-1 max-h-56 w-52 overflow-auto rounded-lg bg-white py-3 text-base shadow ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm')(
                    #                 Li(id='listbox-option-0', role='option', cls='relative cursor-default select-none bg-white px-3 py-2')(
                    #                     Div(cls='flex items-center')(
                    #                         Span('No due date', cls='block truncate font-medium')
                    #                     )
                    #                 ),
                    #                 Li(id='listbox-option-1', role='option', cls='relative cursor-default select-none bg-white px-3 py-2')(
                    #                     Div(cls='flex items-center')(
                    #                         Span('Today', cls='block truncate font-medium')
                    #                     )
                    #                 )
                    #             )
                    #         )
                    #     )
                    # ),
                    Div(cls='flex items-center justify-between space-x-3 border-t border-gray-200 px-2 py-2 sm:px-3')(
                        Div(cls='flex-shrink-0')(
                            Button(
                                'Save', 
                                type='submit', 
                                hx_put=Routes.WORK_ITEM.format(id=self.item.id),
                                target_id=self.base_id,
                                hx_swap='outerHTML', 
                                cls='inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
                                ),
                                Button(
                                'Cancel', 
                                type='reset', 
                                cls='inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600',
                                **{'@click': 'edit_mode=false'}
                                )
                        ),
                    )
                )
            )
        )
    
    def action_buttons(self):
        return Div(cls='flex flex-none items-center gap-x-4', x_show='visible && !edit_mode')(
            self.action(
                'Add Subtask',
                icons.Plus(),
                hx_get = Routes.WORK_ITEM.format(id=self.item.id),
                target_id = f'{self.base_id}-subtasks',
                **{'@click': 'subtasks = !subtasks'}
            ),
            self.action('Edit', icons.Edit(),**{'@click':'edit_mode=true'}),
            self.action(
                'Delete', 
                icons.Delete(), 
                hx_delete=Routes.WORK_ITEM.format(id=self.item.id), 
                hx_swap='outerHTML',
                target_id=self.base_id
            )
        )

    def action(self, alt_text: str, *children, **attributes):
        return A(
            cls='hidden rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:block',
            **attributes
            )(
                *children,
                Span(f', {alt_text}', cls='sr-only'),
            )
    
    def subtasks(self):
        return Div(
            cls = 'ml-10 mr-2',
            x_show = 'subtasks'
            )(
                Div(id=f'{self.base_id}-subtasks'),
                more_items(self.item.id, 0),            
                new_task_input(parent=self.item.id, placeholder='New subtask'), 
            )
    

def more_items(parent: int, page: int, swap: bool = False, hidden:bool = True):
    id = f'work-item-{parent}-children-more'
    hidden_cls = 'hidden' if hidden else ''
    cls = f'{hidden_cls} flex w-full items-center justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline-offset-0'
    url = Routes.WORK_ITEMS if parent == ROOT else Routes.WORK_ITEM.format(id=parent)
    url = url + f'?page={page}'
    target_id = 'work-items' if parent == ROOT else f'work-item-{parent}-subtasks'
    return A(
        'More', 
        id=id,
        href='#', 
        hx_get=url,
        target_id=target_id,
        hx_swap='beforeend',
        hx_swap_oob='true' if swap else False,
        cls=cls
        )
    
def work_items(todos: list[Todo], count_next_page:int, parent: int, page: int):
    hidden_more = count_next_page == 0
    more = more_items(parent, page+1, swap=True, hidden=hidden_more)
    return (Ul(role='list', id="work-items", cls='divide-y divide-gray-100')(
            *[WorkItem(item).render() for item in todos],
            ),
            more)

def new_task_input(parent:int|None = None, placeholder:str = 'New Work Item'):
    post_url = Routes.WORK_ITEMS if parent is None else Routes.WORK_ITEM.format(id=parent)
    target = 'work-items' if parent is None else f'work-item-{parent}-subtasks'
    return Form(
        hx_post=post_url, 
        target_id=target, 
        hx_swap="beforeend",
        hx_on_htmx_after_request='this.reset()'
        )(
        # Label('New Work Item', fr='title', cls='block text-sm font-medium leading-6 text-gray-900'),
        Div(cls='mt-2 flex rounded-md shadow-sm')(
            Div(cls='relative flex flex-grow items-stretch focus-within:z-10')(
                Div(cls='pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3')(
                    icons.Plus()
                ),
                Input(type='text', id='title', placeholder=placeholder, cls='block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6')
            ),
        )
    )
    
