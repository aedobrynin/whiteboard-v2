from . import Font


def test_font_serialization():
    f = Font()
    assert f.serialize() == {
            'slant': 'roman',
            'weight': 'normal',
            'color': 'black',
            'family': 'Arial',
            'size': 14
        }
    f_copy = Font.from_serialized(f.serialize())
    assert f == f_copy


def test_font_update():
    f = Font()
    assert f.serialize() == {
            'slant': 'roman',
            'weight': 'normal',
            'color': 'black',
            'family': 'Arial',
            'size': 14
        }
    f.update_fields(weight='bold', size=15, slant='italic', family='Calibri', color='pink')
    assert f.serialize() == {
        'slant': 'italic',
        'weight': 'bold',
        'color': 'pink',
        'family': 'Calibri',
        'size': 15
    }
