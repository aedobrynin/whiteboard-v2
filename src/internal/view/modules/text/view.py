import internal.objects.interfaces
import internal.view.dependencies


def create_text_object(
    dependencies: internal.view.dependencies.Dependencies,
    obj: internal.objects.interfaces.IBoardObjectText
) -> int:
    return dependencies.canvas.create_text(
        obj.position.x,
        obj.position.y,
        text=obj.text,
        fill=obj.font_color,
        tags=[obj.id, 'text'],
        font=(obj.font_family, int(obj.font_size), obj.font_weight, obj.font_slant)
    )
