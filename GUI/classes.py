import tkinter as tk
from tkinter import ttk
from typing import Callable
from variables import LABEL_FONT, ENTRY_FONT, ROW_COUNT

class Frame(ttk.Frame):
    def __init__(self, master: tk.Tk | ttk.Frame) -> None:
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.int_vcmd = (self.register(self.int_validate), "%d", "%P", "%S")
        self.float_vcmd = (self.register(self.float_validate), "%d", "%P", "%S")
        self._i: int = 0
        self.PADX = 20
        self.PADY = 10
        self.table: ttk.Treeview
        self.table_columns = list()
        self.table_columns_width = list()
        self.table_columns_align = list()
        self.page_no = 1
        self.total_pages = 1
        self.first_entry: tk.Widget
        self.last_entry: tk.Widget

    # ------------------------------------------------ Getter and Setter ------------------------------------------------ #
    @property
    def i(self) -> int:
        self._i += 1
        return self._i - 1

    @i.setter
    def i(self, x) -> None:
        self._i = x
    # ------------------------------------------------------------------------------------------------------------------- #

    def string_entry(self, cls: ttk.Frame, text: str, row: int, column: int, textvariable: tk.StringVar) -> tk.Entry:
        tk.Label(
                cls, text=text, font=LABEL_FONT
            ).grid(
                row=row, column=column,
                padx=self.PADX, pady=self.PADY,
                sticky="e"
        )
        entry = tk.Entry(
                cls, textvariable=textvariable, font=ENTRY_FONT
            )
        entry.grid(
                row=row, column=column+1,
                padx=self.PADX, pady=self.PADY,
                sticky="ew"
        )
        return entry

    def choice_entry(self, cls: ttk.Frame, text: str, row: int, column: int, textvariable: tk.StringVar, choices: list[str]) -> ttk.Combobox:
        tk.Label(
                cls, text=text, font=LABEL_FONT
            ).grid(
                row=row, column=column,
                padx=self.PADX, pady=self.PADY,
                sticky="e"
        )
        choice_box = ttk.Combobox(
            cls, state="readonly", values=choices, textvariable=textvariable, font=ENTRY_FONT
        )
        choice_box.grid(
                row=row, column=column+1,
                padx=self.PADX, pady=self.PADY,
                sticky="ew"
        )
        return choice_box

    def int_entry(self, cls: ttk.Frame, text: str, row: int, column: int, textvariable: tk.StringVar) -> tk.Entry:
        tk.Label(
                cls, text=text, font=LABEL_FONT
            ).grid(
                row=row, column=column,
                padx=self.PADX, pady=self.PADY,
                sticky="e"
        )
        entry = tk.Entry(
                cls, textvariable=textvariable, font=ENTRY_FONT,
                validate="key", validatecommand=self.int_vcmd
            )
        entry.grid(
                row=row, column=column+1,
                padx=self.PADX, pady=self.PADY,
                sticky="ew"
        )
        return entry

    def float_entry(self, cls: ttk.Frame, text: str, row: int, column: int, textvariable: tk.StringVar) -> tk.Entry:
        tk.Label(
                cls, text=text, font=LABEL_FONT
            ).grid(
                row=row, column=column,
                padx=self.PADX, pady=self.PADY,
                sticky="e"
        )
        entry = tk.Entry(
                cls, textvariable=textvariable, font=ENTRY_FONT,
                validate="key", validatecommand=self.float_vcmd
            )
        entry.grid(
                row=row, column=column+1,
                padx=self.PADX, pady=self.PADY,
                sticky="ew"
        )
        return entry

    def date_entry(self, cls: ttk.Frame, text: str, row: int, column: int, monthvar: tk.IntVar, yearvar: tk.IntVar) -> None:
        tk.Label(
                cls, text=text, font=LABEL_FONT
            ).grid(
                row=row, column=column,
                padx=self.PADX, pady=self.PADY,
                sticky="e"
        )
        tk.Spinbox(
                cls, from_=1, to=12, textvariable=monthvar, font=ENTRY_FONT,
                validate="key", validatecommand=self.int_vcmd
            ).grid(
                row=row, column=column+1,
                padx=self.PADX, pady=self.PADY,
                sticky="ew"
        )
        tk.Spinbox(
                cls, from_=2000, to=2999, textvariable=yearvar, font=ENTRY_FONT,
                validate="key", validatecommand=self.int_vcmd
            ).grid(
                row=row, column=column+2,
                padx=self.PADX, pady=self.PADY,
                sticky="ew"
        )

    def create_button(self, cls: ttk.Frame, text: str, row: int, column: int, width: int, bg: str, func: Callable) -> tk.Button:
        btn = tk.Button(
                cls, text=text, width=width, command=func,
                font=LABEL_FONT, bg=bg
            )
        btn.grid(
                row=row, column=column,
                padx=self.PADX*2, pady=self.PADY*2,
                ipadx=10, ipady=10,
                sticky="e"
        )
        return btn

    def create_table(self, cls: ttk.Frame, row: int, column: int) -> None:
        self.table = ttk.Treeview(
            cls, show="headings", selectmode="browse",
            columns=self.table_columns, height=ROW_COUNT
        )
        for col_name, col_width, col_align in zip(self.table_columns, self.table_columns_width, self.table_columns_align):
            self.table.heading(col_name, text=col_name)
            self.table.column(col_name, width=col_width, anchor=col_align)
        self.table.grid(row=row, column=column, padx=self.PADX, pady=self.PADY, sticky="nsew")

    # ------------------------------------------------ Input Validation ------------------------------------------------ #
    def int_validate(self, action: str, current_value: str, current_input: str) -> bool:
        if (action != '1'):
            return True
        if (current_input not in "0123456789"):
            return False
        try:
            int(current_value)
            return True
        except ValueError:
            return False

    def float_validate(self, action: str, current_value: str, current_input: str) -> bool:
        if (action != '1'):
            return True
        if (current_input not in "0123456789."):
            return False
        try:
            float(current_value)
            return True
        except ValueError:
            return False
    # ------------------------------------------------------------------------------------------------------------------ #

    def tab_sequencing(self):
        self.first_entry.bind("<Shift-Tab>", lambda x: self.last_entry.focus_set() or "break")
        self.last_entry.bind("<Tab>", lambda x: (self.first_entry.focus_set() or "break") if x.state!=9 else None)

    def refresh(self) -> None:
        pass

    def events(self) -> None:
        pass

    def set_active(self) -> None:
        self.tkraise()
        self.refresh()
