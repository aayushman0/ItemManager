import tkinter as tk
from tkinter import ttk
from db.orm import product
from GUI import classes


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        pass

    def main(self) -> None:
        pass

    # def events(self) -> None:
    #     self.tab_sequencing()

    # def refresh(self) -> None:
    #     self.first_entry.focus_set()
