import tkinter

from . import context


def on_drag_start(ctx: context.Context, event: tkinter.Event):
    ctx.canvas.scan_mark(event.x, event.y)


def on_dragging(ctx, event):
    ctx.canvas.scan_dragto(event.x, event.y, gain=1)


def bind_on_events(ctx: context.Context):
    ctx.canvas.bind('<ButtonPress-1>', lambda event: on_drag_start(ctx, event))
    ctx.canvas.bind('<B1-Motion>', lambda event: on_dragging(ctx, event))
