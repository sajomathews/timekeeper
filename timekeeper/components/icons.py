from fasthtml.ft import *
from timekeeper.components.custom_ft import *

def Plus(**attributes):
    attributes['cls'] = attributes.get('cls', 'size-4')
    return Svg(xmlns='http://www.w3.org/2000/svg', fill='none', viewbox='0 0 24 24', stroke_width='1.5', stroke='currentColor', **attributes)(
        Path(stroke_linecap='round', stroke_linejoin='round', d='M12 4.5v15m7.5-7.5h-15')
    )

def Edit(**attributes):
    attributes['cls'] = attributes.get('cls', 'size-4')
    return Svg(xmlns='http://www.w3.org/2000/svg', fill='none', viewbox='0 0 24 24', stroke_width='1.5', stroke='currentColor', **attributes)(
        Path(stroke_linecap='round', stroke_linejoin='round', d='m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10')
    )

def Delete(**attributes):
    attributes['cls'] = attributes.get('cls', 'size-4')
    return Svg(xmlns='http://www.w3.org/2000/svg', fill='none', viewbox='0 0 24 24', stroke_width='1.5', stroke='currentColor', **attributes)(
        Path(stroke_linecap='round', stroke_linejoin='round', d='m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0')
    )

def Logo(**attributes):
    attributes['cls'] = attributes.get('cls', 'size-12')
    return Svg(xmlns='http://www.w3.org/2000/svg', viewbox='0 0 150 150', stroke_width='4', stroke='currentColor',  **attributes)(
        Circle(cx='75', cy='75', r='48', stroke='#6366f1', stroke_width='8', fill='#EEFFFF'),
        Line(x1='75', y1='75', x2='55', y2='55', stroke='#6366f1', stroke_width='4'),
        Line(x1='75', y1='75', x2='100', y2='60', stroke='#6366f1', stroke_width='4'),
        Circle(cx='30', cy='100', r='25', stroke='#ffffff', stroke_width='4', fill='#6366f1'),
        Path(d='M20,100 l8,8 l15,-15', stroke='#ffffff', stroke_width='4', fill='none'),
        Polygon(fill='#6366f1', stroke='none', stroke_width='2', stroke_miterlimit='10', points='32,1 26,1 26,10 20,12 14,6 6,14 12,20,10,26 1,26 1,38 10,38 12,44 6,50 14,58 20,52 26,54 26,63 32,63 38,63 38,54 44,52 50,58 58,50 52,44 54,38 63,38 63,26 54,26,52,20 58,14 50,6 44,12 38,10 38,1'),
        Circle(fill='none', stroke='#ffffff', stroke_width='2', stroke_miterlimit='10', cx='32', cy='32', r='6')
        #Text('Timekeeper', x='50', y='85', font_family='sans-serif', font_size='10', text_anchor='middle', fill='#4A90E2')
    )

def Menu(**attributes):
    attributes['cls'] = attributes.get('cls', 'h-5 w-5')
    return Svg(xmlns='http://www.w3.org/2000/svg', fill='none', viewbox='0 0 24 24', stroke='currentColor',  **attributes)(
        Path(stroke_linecap='round', stroke_linejoin='round', stroke_width='2', d='M4 6h16M4 12h8m-8 6h16')
    )

def Sun(**attributes):
    attributes['cls'] = attributes.get('cls', 'size-4')
    return Svg(xmlns='http://www.w3.org/2000/svg', viewbox='0 0 24 24', **attributes)(
        Path(d='M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z')
    )

def Moon(**attributes):
    attributes['cls'] = attributes.get('cls', 'size-4')
    return Svg(xmlns='http://www.w3.org/2000/svg', viewbox='0 0 24 24', **attributes)(
        Path(d='M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z')
    )