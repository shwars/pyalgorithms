# Python Algorithm Visualizer Helper

import ipywidgets as widgets
from IPython.display import display, clear_output
import time,timeit

def disp_array_box(l,highlight=None,highlight_color='lightblue',boundaries=None):
    def h(x): 
        return f' style="background-color: {highlight_color}"' \
           if highlight is not None and x in highlight else ""
    def b(x):
        return "↑" if x in boundaries else "&nbsp;"
    bound = "" if boundaries is None else '<table border="0"><tr>'+''.join([f'<td width="25" height="15" align="center">{b(i)}</td>' for i,x in enumerate(l)])+'</tr></table>'
    return widgets.HTML('<table border="1"><tr>' +
        ''.join([f'<td width="25" height="15" align="center"{h(i)}>{x}</td>' for i,x in enumerate(l)]) +
        f'</tr></table>{bound}')

def disp_array_lines(l,highlight=None,color='red', highlight_color='blue', scale=50):
    return widgets.HTML('<div>' +
        ''.join([f'<div style="background:{highlight_color if highlight is not None and i in highlight else color}; width:{x*scale}px; height:10px; margin:2px;"></div>' for i,x in enumerate(l)]) +
        '</div>')

def display_array(l,kind='box',highlight=None,highlight_value=None,scale=50,highlight_color='lightblue',color='red',replace_none='N',boundaries=None):
    if highlight_value and not highlight:
        highlight=[]
        for i,x in enumerate(l):
            if x==highlight_value or (x is None and highlight_value=='None'):
                highlight.append(i)
    if replace_none:
        l = l.copy()
        for i,x in enumerate(l):
            if x is None:
                l[i] = replace_none
    if kind=='box':
        display(disp_array_box(l,highlight=highlight,highlight_color=highlight_color,boundaries=boundaries))
    elif kind=='bar':
        display(disp_array_lines(l,highlight=highlight,scale=scale,highlight_color=highlight_color,color=color))
    else:
        raise "Use kind='box' or kind='bar'"



class SortVisualizer():
    visualization = True
    def __init__(self,array=None, delay=0, kind='box', width=700):
        self.out = widgets.Output()
        self.delay = delay
        self.kind = kind
        self.scale = width // max(array) if array else 0
        if self.scale==0:
            self.scale = 1
        if SortVisualizer.visualization:
            display(self.out)
            if array: 
                with self.out:
                    display_array(array,kind=kind)
                    clear_output(wait=True)
        
    def visualize(self,l,delay=None,swap=None,boundaries=None):
        if not SortVisualizer.visualization:
            return
        delay = delay if delay else self.delay
        with self.out:
            if swap:
                display_array(l,highlight=swap,scale=self.scale,boundaries=boundaries,kind=self.kind)
                clear_output(wait=True)
                time.sleep(delay)
            display_array(l,scale=self.scale,boundaries=boundaries,kind=self.kind)
            if delay>0:
                time.sleep(delay)
            clear_output(wait=True)

    def visualize2(self,l1,l2,title1=None,title2=None,delay=None,highlight_value=None):
        if not SortVisualizer.visualization:
            return
        delay = delay if delay else self.delay
        with self.out:
            if title1: display(widgets.HTML(f"<b>{title1}</b><br/>"))
            display_array(l1,scale=self.scale,highlight_value=highlight_value,kind=self.kind)
            if title2: display(widgets.HTML(f"<b>{title2}</b><br/>"))
            display_array(l2,scale=self.scale,highlight_value=highlight_value,kind=self.kind)
            if delay>0:
                time.sleep(delay)
            clear_output(wait=True)

    @classmethod
    def set_visualization(cls,visualize):
        cls.visualization = visualize

    @staticmethod
    def time_execution_table(functions,data,funclabels=None,datalabels=None,number=5,globals=globals()):
        def time_exec(func,data):
            return timeit.timeit(stmt=f'{func}({data})',number=number,globals=globals)
        def row(func,funclab,data):
            return (f'<tr><td><b>{funclab}</b></td>'+
              ''.join([f'<td>{time_exec(func,x):.4f}</td>' for x in data])+
              '</tr>');
        if not funclabels:
            funclabels = functions
        if not datalabels:
            datalabels = map(str,data)
        display(widgets.HTML('<table border="2" cellpadding="3"><tr><td></td>'+''.join([f'<td><b>{x}</b></td>' for x in datalabels])+'</tr>'+
        ''.join(row(func,funclab,data) for func,funclab in zip(functions,funclabels))+'</table>'))

