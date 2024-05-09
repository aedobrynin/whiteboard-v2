from internal.models.font import Font as ObjectFont


def as_object_font(name: str, color: str):
    # TODO: parser
    family, size, weight, slant = name.split()
    return ObjectFont(
        slant,
        weight,
        color,
        family,
        int(size)
    )


def as_tkinter_font(name: str):
    # TODO: parser
    family, size, weight, slant = name.split()
    return family, int(size), weight, slant


def as_tkinter_object_font(font: ObjectFont):
    return font.family, int(font.size), font.weight, font.slant
