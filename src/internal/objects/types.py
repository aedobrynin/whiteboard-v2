import enum


class BoardObjectType(enum.Enum):
    TEXT = 'text'
    CARD = 'card'
    PEN = 'pen'
    GROUP = 'group'
    CONNECTOR = 'connector'
    TABLE = 'table'
    CODE = 'code'
