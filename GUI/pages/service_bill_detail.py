import tkinter as tk
from tkinter import ttk, messagebox
from db.orm import service_bill
from GUI import classes
from variables import BILL_ROW_COUNT, ENTRY_FONT


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.table_columns = ["Name", "Price"]
        self.table_columns_width = [300, 200]
        self.table_columns_align = ["w", "n"]
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.bill_no = tk.StringVar()
        self.bill_date = tk.StringVar()
        self.customer_name = tk.StringVar()
        self.sum_total = tk.StringVar()
        self.discount = tk.StringVar()
        self.net_total = tk.StringVar()

    def main(self) -> None:
        entry_frame = ttk.Frame(self)
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.grid(row=0, sticky="ew")
        tk.Button(
                entry_frame, text="<", width=10, height=1, font=ENTRY_FONT, bg="#dddddd", command=self.return_prev_page
            ).grid(
                row=0, column=0, padx=self.PADX, sticky="w"
        )
        self.string_entry(entry_frame, "Bill No.: ", 0, 1, self.bill_no).config(state="disabled")
        self.string_entry(entry_frame, "Bill Date: ", 0, 4, self.bill_date).config(state="disabled")
        self.string_entry(entry_frame, "Customer's Name: ", 1, 0, self.customer_name, 5).config(state="disabled")
        self.string_entry(entry_frame, "Sum Total: ", 2, 0, self.sum_total).config(state="disabled")
        self.string_entry(entry_frame, "Discount: ", 2, 2, self.discount).config(state="disabled")
        self.string_entry(entry_frame, "Net Total: ", 2, 4, self.net_total).config(state="disabled")

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=1, sticky="ew")
        self.create_table(table_frame, 0, 0)
        self.table.config(height=BILL_ROW_COUNT)

        edit_frame = ttk.Frame(self)
        edit_frame.grid(row=2, sticky="e")
        self.create_button(edit_frame, "Delete Bill", 0, 0, 30, "#ffd0d0", self.delete_bill)

    def events(self) -> None:
        pass

    def delete_bill(self) -> None:
        bill_no = self.bill_no.get()
        if not bill_no:
            return None
        confirmation = messagebox.askyesno(title="Delete Bill", message=f"Delete Bill no. {bill_no}?")
        if not confirmation:
            return None
        b = service_bill.delete(bill_no)
        if not b:
            return None
        if b.is_enabled:
            messagebox.showwarning("Bill not Deleted", "Bill cannot be deleted!")
            return None
        self.return_prev_page()

    def refresh(self) -> None:
        self.table.delete(*self.table.get_children())
        bill_no = self.bill_no.get()
        bill = service_bill.get(bill_no)
        if not bill:
            messagebox.showwarning("Bill not Found", "Bill cannot be found!")
            self.bill_date.set("XXXX-XX-XX")
            self.customer_name.set("")
            self.discount.set("")
            self.net_total.set("")
            return None
        self.bill_date.set(bill.bill_date)
        self.customer_name.set(bill.customer_name)
        self.sum_total.set(bill.total_amount)
        self.discount.set(bill.discount)
        self.net_total.set(bill.net_amount)
        bill_list = bill.bill.split(",")
        for b in bill_list:
            self.table.insert('', tk.END, values=b.split("::"))
