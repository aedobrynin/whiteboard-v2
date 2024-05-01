import internal.objects.interfaces
import internal.view.dependencies

TEXT_PREFIX = 'text'


def create_text_object(
    dependencies: internal.view.dependencies.Dependencies,
    obj: internal.objects.interfaces.IBoardObjectText
) -> None:
    dependencies.canvas.create_text(
        obj.position.x,
        obj.position.y,
        text=obj.text,
        fill=obj.font.color,
        tags=[obj.id, f'{TEXT_PREFIX}{obj.id}'],
        font=(obj.font.family, int(obj.font.size), obj.font.weight, obj.font.slant)
    )
