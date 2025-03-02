import tkinter as tk
from tkinter import ttk
from db.orm import product
from GUI import classes


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
