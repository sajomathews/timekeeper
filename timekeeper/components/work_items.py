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
            cls='bg-base-100 flex flex-col items-center justify-between gap-y-6 py-2', 
            id=self.base_id,
            x_data = '{visible: false, edit_mode: false, subtasks: false}',
            )(
                Div(cls='w-full overflow-hidden rounded-lg')(
                    Div(cls='px-2 py-2 sm:p-2')(
                        *children
                    )       
                )
            )
    
    def flex_row(self, *children, **attributes):
        return Div(cls='min-h-14 w-full flex flex-row items-center justify-between gap-x-6 py-1', **attributes)(*children)
    
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
                        cls='checkbox checkbox-success',
                        hx_patch=Routes.WORK_ITEM_COMPLETED.format(id=self.item.id),
                        target_id=self.base_id,
                        hx_swap='outerHTML',
                        hx_vals = vals
                    )
                ),
                Div(cls='ml-3 text-sm leading-6')(
                    Label(
                        fr=id, 
                        cls='font-medium font-semibold leading-6 text-base-content text-base'
                    )(
                        self.item.title, 
                        self.percent_complete(),
                    ),
                    P(self.item.description, cls='text-base-content text-sm')
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
        swap_value = 'true' if swap else None
        return Div(id=f'{self.base_id}-percent-complete',hx_swap_oob=swap_value)(
            Progress(
                cls='progress progress-success w-32', 
                value=self.item.percent_complete*100, 
                max=100, 
            ), 
            Span(cls='text-xs')(f'{self.item.percent_complete*100:0.1f}%')
        )
        
    def edit_form(self):
        id_base = self.base_id
        return Div(cls='min-w-0 w-full', x_show='edit_mode')(
            Form(action='#', cls='relative')(
                Div(cls='overflow-hidden rounded-lg border border-primary shadow-sm focus-within:border-indigo-500 focus-within:ring-1 focus-within:ring-indigo-500')(
                    Label('Title', fr=f'{id_base}-title', cls='sr-only'),
                    Input(type='text', name='title', id=f'{id_base}-title', value=self.item.title, placeholder='Title', cls='input w-full focus:outline-none focus:border-0 text-lg'),
                    Label('Description', fr=f'{id_base}-description', cls='sr-only'),
                    Textarea(
                        rows='2', 
                        name='description',
                        id=f'{id_base}-description',
                        placeholder='Write a description ...',
                        cls='textarea w-full mb-10 resize-none focus:ring-0 focus:outline-none border-0 text-sm'
                    )(
                        self.item.description
                    ),
                ),
                Div(cls='absolute inset-x-px bottom-0')(
                    Div(cls='my-2 mx-4')(
                        Button(
                            'Save',
                            type='submit',
                            hx_put=Routes.WORK_ITEM.format(id=self.item.id),
                            target_id=self.base_id,
                            hx_swap='outerHTML', 
                            cls='btn btn-primary btn-sm rounded-sm mr-2'
                        ),
                        Button(
                            'Cancel',
                            type='reset',
                            cls='btn btn-neutral btn-sm rounded-sm',
                            **{'@click': 'edit_mode=false'}
                        )
                    )
                )
            )
        )
    
    def action_buttons(self):
        return Div(cls='join', x_show='visible && !edit_mode')(
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
                target_id=self.base_id,
                hx_confirm=f"Are you sure you want to delete this task and all it's subtasks?\n '{self.item.title}'",
            )
        )

    def action(self, alt_text: str, *children, **attributes):
        return Button(
            cls = 'btn join-item',
            **attributes
        )(
            *children,
            Span(f', {alt_text}', cls='sr-only')
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
    cls = f'{hidden_cls} btn w-full'
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
    return Ul(
        cls='card divide-y divide-base-300',
        id='work-items',
    )(
        *[WorkItem(item).render() for item in todos]
    ), more
    # return (
    #     Div(role='list', id="work-items", cls='divide-y divide-gray-100')(
    #         *[WorkItem(item).render() for item in todos],
    #     ),
    #     more
    # )

def new_task_input(parent:int|None = None, placeholder:str = 'New Work Item'):
    post_url = Routes.WORK_ITEMS if parent is None else Routes.WORK_ITEM.format(id=parent)
    target = 'work-items' if parent is None else f'work-item-{parent}-subtasks'
    return Form(
        hx_post=post_url, 
        target_id=target, 
        hx_swap="beforeend",
        hx_on_htmx_after_request='this.reset()',
        cls='form-control'
        )(
            Label(cls='my-1 input input-bordered flex items-center gap-2')(
                Input(type='text', id='title', cls='grow', placeholder=placeholder),
                icons.Plus()
            ),
    )
    
