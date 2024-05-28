import tkinter
import internal.view.modules.modules
import internal.view.dependencies


def zoom_on_wheel(
    dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
):
    print(event, event.num, event.delta)
    x = dependencies.canvas.canvasx(event.x)
    y = dependencies.canvas.canvasy(event.y)
    scale = dependencies.scaler

    # Respond to Linux (event.num) or Windows (event.delta) wheel event
    if event.num == 5 or event.delta == -120:  # scroll down
        scale *= 0.9
        scale = max(scale, 0.2)  #
        print(scale)
    if event.num == 4 or event.delta == 120:  # scroll up
        scale *= 1.1
        scale = min(scale, 4.0)  # 400%
        print(scale)
    diff_scale = scale / dependencies.scaler
    print(diff_scale)
    dependencies.scaler = scale
    dependencies.canvas.scale(tkinter.ALL, x, y, diff_scale, diff_scale)
    for obj in dependencies.objects_storage.get_objects().values():
        obj.scale(dependencies)


def bind_on_events(dependencies: internal.view.dependencies.Dependencies):
    dependencies.canvas.bind(
        '<Control-MouseWheel>', lambda event: zoom_on_wheel(dependencies, event)
    )  # Win + MacOS
    dependencies.canvas.bind(
        '<Control-Button-5>', lambda event: zoom_on_wheel(dependencies, event)
    )  # Linux
    dependencies.canvas.bind(
        '<Control-Button-4>', lambda event: zoom_on_wheel(dependencies, event)
    )  # Linux


@internal.view.modules.modules.register_module('zoom_board')
def init_module(dependencies: internal.view.dependencies.Dependencies):
    bind_on_events(dependencies)
