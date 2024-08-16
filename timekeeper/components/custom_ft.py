from fasthtml.common import ft_hx
from fasthtml.components import Circle, Text, Line, Polygon


def Path(*c, target_id=None, **kwargs): 
    return ft_hx('path', *c, target_id=target_id, **kwargs)