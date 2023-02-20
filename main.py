import PySimpleGUI as sg
import psutil
import numpy as np

def plot(graph: sg.Graph, x_axis: list[int | float], y_axis: list[int | float], color='black'):
    prev_x: int | None
    prev_y: int | float | None

    i: int
    x_coord: int
    y_coord: int | float

    prev_x = prev_y = None
    for i, x_coord in enumerate(x_axis):
        y_coord = y_axis[i]
        if prev_x is not None and prev_y is not None:                
            graph.draw_line((prev_x, prev_y), (x_coord, y_coord),
                            color=color, width=1.5)
        prev_x, prev_y = x_coord, y_coord

graph: sg.Graph = sg.Graph(
    canvas_size=(600, 100),
    graph_bottom_left=(0, 0),
    graph_top_right=(200, 100),
    background_color='gray',
    key='-CPU-USAGE-GRAPH-'
)

cpus: list[list[sg.T | sg.Progress]] = [
    [sg.T(f'CPU #{i + 1}'), sg.Progress(key=f'-CPU-{i}-USAGE-', max_value=100, orientation='h', size=(50, 5))] 
        for i in range(psutil.cpu_count())]

window: sg.Window = sg.Window('CPU Monitor', [
    *cpus,
    [graph]
], keep_on_top=True, finalize=True, grab_anywhere=True)

colors: list[str] = [
    'white', 'purple', 'blue', 'orange'
]

y_data: list[list[float]] = [
    [], [], [], []
]
values: dict

while True:
    event, values = window.read(timeout=1000 / 3)

    if event in (sg.WIN_CLOSED,):
        break

    graph.erase()

    cpu_percent: float
    i: int
    for i, cpu_percent in enumerate(psutil.cpu_percent(1 / 3, percpu=True)):
        color = ('darkgreen' if cpu_percent < 33
                else 'yellow' if cpu_percent < 66
                else 'red')

        y_data[i].append(cpu_percent)

        plot(graph, [i for i in range(len(y_data[i]))], y_data[i], color=colors[i])

        window[f'-CPU-{i}-USAGE-'].update(cpu_percent, bar_color=(colors[i], color))
        
window.close()
