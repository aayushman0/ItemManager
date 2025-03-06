import tkinter as tk
from db.orm import product
from GUI import classes
from variables import PRODUCT_TYPES_LIST


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(1, weight=1)
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.product_name = tk.StringVar()
        self.product_type = tk.StringVar()
        self.product_price = tk.StringVar()
        self.product_min_unit = tk.StringVar()
        self.product_best_before = tk.StringVar()
        self.product_shelf_id = tk.StringVar()

    def main(self) -> None:
        self.first_entry = self.string_entry(self, "Name: ", self.i, 0, self.product_name)
        self.type_entry = self.choice_entry(self, "Type: ", self.i, 0, self.product_type, PRODUCT_TYPES_LIST)
        self.float_entry(self, "Price: ", self.i, 0, self.product_price)
        self.int_entry(self, "Min. Unit: ", self.i, 0, self.product_min_unit)
        self.int_entry(self, "Best Before: ", self.i, 0, self.product_best_before)
        self.string_entry(self, "Shelf ID: ", self.i, 0, self.product_shelf_id)
        self.last_entry = self.create_button(self, "Add Item", self.i, 1, 30, "#d0ffd0", self.add_product)

    def events(self) -> None:
        self.tab_sequencing()

    def add_product(self) -> None:
        name = self.product_name.get()
        type = self.product_type.get()
        price = self.product_price.get()
        min_unit = self.product_min_unit.get()
        best_before = self.product_best_before.get()
        shelf = self.product_shelf_id.get()
        if not (name and type and price and min_unit and best_before and shelf):
            print("Value missing!!!")
            return None
        try:
            _ = product.create(
                name=name,
                type=type,
                price=float(price),
                min_unit=int(min_unit),
                best_before=int(best_before),
                shelf=shelf
            )
            self.refresh()
        except product.ProductAlreadyExists:
            print("Product already exist!!!")

    def refresh(self) -> None:
        self.product_name.set("")
        self.type_entry.current(0)
        self.product_price.set("")
        self.product_min_unit.set("")
        self.product_best_before.set("")
        self.product_shelf_id.set("")
        self.first_entry.focus_set()
