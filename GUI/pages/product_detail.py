import tkinter as tk
from db.orm import product
from GUI.pages import add_product
from variables import PRODUCT_TYPES_LIST


class Frame(add_product.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.product_id = tk.StringVar()

    def main(self) -> None:
        self.first_entry = self.string_entry(self, "Name: ", self.i, 0, self.product_name)
        self.type_entry = self.choice_entry(self, "Type: ", self.i, 0, self.product_type, PRODUCT_TYPES_LIST)
        self.float_entry(self, "Price: ", self.i, 0, self.product_price)
        self.int_entry(self, "Min. Unit: ", self.i, 0, self.product_min_unit)
        self.int_entry(self, "Best Before: ", self.i, 0, self.product_best_before)
        self.string_entry(self, "Shelf ID: ", self.i, 0, self.product_shelf_id)
        self.last_entry = self.create_button(self, "Edit Item", self.i, 1, 30, "#d0ffd0", self.edit_product)

    def edit_product(self) -> None:
        if not self.product_id.get():
            return None
        name = self.product_name.get()
        type = self.product_type.get()
        price = self.product_price.get()
        min_unit = self.product_min_unit.get()
        best_before = self.product_best_before.get()
        shelf = self.product_shelf_id.get()
        if not (name and type and price and min_unit and best_before and shelf):
            print("Value missing!!!")
            return None
        p = product.edit(
            id=self.product_id.get(),
            name=name,
            type=type,
            price=price,
            min_unit=min_unit,
            best_before=best_before,
            shelf=shelf
        )
        if not p:
            print("Error!!!")
            return None
        self.refresh()

    def refresh(self) -> None:
        p = product.get_by_id(self.product_id.get())
        if p:
            self.product_name.set(p.name)
            self.type_entry.current(PRODUCT_TYPES_LIST.index(p.type))
            self.product_price.set(p.price)
            self.product_min_unit.set(p.min_unit)
            self.product_best_before.set(p.best_before)
            self.product_shelf_id.set(p.shelf)
        else:
            self.product_name.set("")
            self.type_entry.current(0)
            self.product_price.set("")
            self.product_min_unit.set("")
            self.product_best_before.set("")
            self.product_shelf_id.set("")
        self.first_entry.focus_set()
