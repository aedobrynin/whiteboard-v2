import pathlib
import tkinter
import uuid
from tkinter import ttk

import pyperclip


def _load_from_file(path_to_file: pathlib.Path):
    with open(path_to_file, 'r') as file:
        res = [list(line.split('#')) for line in file]
        board_names_keys = {str(line[0]): str(line[1]) for line in res}

    return board_names_keys


def _is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def _create_new_board(
    board_name_entry: ttk.Entry,
    board_key_entry: ttk.Entry,
    listbox: tkinter.Listbox,
    path_to_file: str,
    available_boards: dict,
):
    board_name = board_name_entry.get()
    board_name_entry.delete(0, tkinter.END)

    board_key = board_key_entry.get()
    board_key_entry.delete(0, tkinter.END)
    if not board_name or not board_name.isprintable():
        return
    for existing_boards in listbox.get(0, tkinter.END):
        if board_name == existing_boards:
            return

    if not board_key or not board_name.isprintable() or not _is_valid_uuid(board_key):
        board_key = str(uuid.uuid4())
    with open(path_to_file, 'a') as file:
        if available_boards:
            file.write('\n')
        file.write(board_name + '#' + board_key)
    available_boards[board_name] = board_key

    listbox.insert(tkinter.END, board_name)


def _set_buttons_state_to_normal(open_button: ttk.Button, copy_key_button: ttk.Button):
    open_button['state'] = 'normal'
    copy_key_button['state'] = 'normal'


def _copy_key(available_boards: dict, boards_listbox: tkinter.Listbox):
    selected_board = boards_listbox.curselection()
    selected_board_name = boards_listbox.get(selected_board)
    selected_board_key = available_boards[selected_board_name]
    pyperclip.copy(selected_board_key)  # Копирует в буфер обмена информацию
    pyperclip.paste()


def get_board_name_key():
    window = tkinter.Tk(className='Choose board')
    window.geometry('600x300')

    path_to_file = 'boards.txt'

    available_boards = _load_from_file(path_to_file)
    boards_listbox = tkinter.Listbox()
    boards_listbox.grid(row=2, column=0, columnspan=3, sticky=tkinter.EW, padx=5, pady=5)
    for board_name in available_boards.keys():
        boards_listbox.insert(tkinter.END, board_name)

    new_board_name_entry = ttk.Entry()
    new_board_name_entry.grid(column=1, row=0, padx=6, pady=6, sticky=tkinter.EW)
    board_name_label = ttk.Label(text='Название доски')
    board_name_label.grid(column=0, row=0, padx=6, pady=6, sticky=tkinter.EW)

    new_board_key_entry = ttk.Entry()
    new_board_key_entry.grid(column=1, row=1, padx=6, pady=6, sticky=tkinter.EW)
    board_key_label = ttk.Label(text='Ключ доступа, если есть')
    board_key_label.grid(column=0, row=1, padx=6, pady=6, sticky=tkinter.EW)

    create_button = ttk.Button(
        text='Создать новую доску',
        command=lambda board_name_entry_arg=new_board_name_entry, board_key_entry_arg=new_board_key_entry, boards_listbox_arg=boards_listbox, path_to_file_arg=path_to_file, available_boards_arg=available_boards: _create_new_board(
            board_name_entry_arg,
            board_key_entry_arg,
            boards_listbox_arg,
            path_to_file_arg,
            available_boards_arg,
        ),
    )
    create_button.grid(column=2, row=1, padx=6, pady=6)

    open_button = ttk.Button(
        text='Открыть выбранную доску', command=lambda window_arg=window: window_arg.quit()
    )
    open_button.grid(row=3, column=2, padx=5, pady=5)
    open_button['state'] = 'disabled'

    copy_key_button = ttk.Button(
        text='Скопировать ключ доски',
        command=lambda available_boards_arg=available_boards, boards_listbox_arg=boards_listbox: _copy_key(
            available_boards_arg, boards_listbox_arg
        ),
    )
    copy_key_button.grid(row=3, column=0, padx=5, pady=5)
    copy_key_button['state'] = 'disabled'

    boards_listbox.bind(
        '<<ListboxSelect>>',
        lambda _, open_button_arg=open_button, copy_key_button_arg=copy_key_button: _set_buttons_state_to_normal(
            open_button_arg, copy_key_button_arg
        ),
    )

    window.mainloop()
    selected_board = boards_listbox.curselection()
    selected_board_name = boards_listbox.get(selected_board)
    selected_board_key = available_boards[selected_board_name]
    window.destroy()
    return selected_board_name, selected_board_key
