import tkinter as tk
from tkinter import ttk, messagebox
from db.orm import service_bill
from GUI import classes
from variables import ENTRY_FONT, BILL_ROW_COUNT


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.table_columns = ["Name", "Price"]
        self.table_columns_width = [300, 200]
        self.table_columns_align = ["w", "n"]
        self.bill_list = list()
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.customer_name = tk.StringVar()
        self.service_name = tk.StringVar()
        self.price = tk.StringVar()
        self.sum_total = tk.StringVar()
        self.discount = tk.StringVar()
        self.net_total = tk.StringVar()

    def main(self) -> None:
        entry_frame = ttk.Frame(self)
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.grid(row=0, sticky="ew")
        self.first_entry = self.string_entry(entry_frame, "Customer's Name: ", 0, 0, self.customer_name, 2)
        self.service_entry = self.string_entry(entry_frame, "Service Name: ", 1, 0, self.service_name, 2)
        self.float_entry(entry_frame, "Price: ", 2, 0, self.price)
        tk.Button(
                entry_frame, text="Add to Bill", width=20, height=1, font=ENTRY_FONT, bg="#ababdf", command=self.add_to_bill
            ).grid(
                row=2, column=2, padx=self.PADX, sticky="w"
        )

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=1, sticky="ew")
        self.create_table(table_frame, 0, 0)
        self.table.config(height=BILL_ROW_COUNT)

        bottom_frame = ttk.Frame(self)
        bottom_frame.columnconfigure(4, weight=1)
        bottom_frame.grid(row=2, sticky="ew")
        self.float_entry(bottom_frame, "Sum Total: ", 0, 0, self.sum_total).config(state="disabled")
        self.float_entry(bottom_frame, "Discount: ", 0, 2, self.discount)
        self.float_entry(bottom_frame, "Net Total: ", 1, 0, self.net_total).config(state="disabled")
        self.last_entry = self.create_button(bottom_frame, "Save Bill", 0, 4, 30, "#d0ffd0", self.add_bill)
        self.last_entry.grid_configure(rowspan=2)

    def events(self) -> None:
        self.tab_sequencing()
        self.discount.trace_add("write", self.calculate_net_total)
        self.table.bind("<Double-Button-1>", self.remove_from_bill)

    def add_to_bill(self) -> None:
        service_name = self.service_name.get().replace(",", "")
        price = float(self.price.get() or 0)
        if not (service_name and price):
            messagebox.showwarning("Missing Values", "Values are missing!")
            return None
        self.table.insert('', tk.END, values=(service_name, price))
        self.bill_list.append(f"{service_name}::{price}")
        sum_total = float(self.sum_total.get() or 0)
        self.sum_total.set(sum_total + price)
        self.refresh_entry()
        self.calculate_net_total()
        self.service_entry.focus_set()

    def add_bill(self) -> None:
        if not self.bill_list:
            messagebox.showwarning("Empty Bill", "Bill is Empty!")
            return None
        bill_string = ",".join(self.bill_list)
        customer_name = self.customer_name.get()
        total_amount = float(self.sum_total.get() or 0)
        discount = float(self.discount.get() or 0)
        net_amount = float(self.net_total.get() or 0)
        service_bill.create(
            customer_name=customer_name,
            bill_string=bill_string,
            total_amount=total_amount,
            discount=discount,
            net_amount=net_amount
        )
        self.refresh()

    def calculate_net_total(self, *args) -> None:
        sum_total = float(self.sum_total.get() or 0)
        discount = float(self.discount.get() or 0)
        total = max(sum_total - discount, 0)
        self.net_total.set(f"{total:.2f}")

    def remove_from_bill(self, *args) -> None:
        cur_item = self.table.focus()
        if not cur_item:
            return None
        i = self.table.index(cur_item)
        self.table.delete(cur_item)
        removed_item: str = self.bill_list.pop(i)
        item_total = float(removed_item.split("::")[1] or 0)
        sum_total = float(self.sum_total.get() or 0)
        self.sum_total.set(sum_total - item_total)
        self.calculate_net_total()

    def refresh_entry(self) -> None:
        self.service_name.set("")
        self.price.set("")

    def refresh(self) -> None:
        self.customer_name.set("")
        self.refresh_entry()
        self.bill_list = []
        self.table.delete(*self.table.get_children())
        self.sum_total.set("")
        self.discount.set("")
        self.net_total.set("")
