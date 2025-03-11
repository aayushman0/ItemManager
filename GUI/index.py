import tkinter as tk
from tkinter import ttk
from GUI.pages import add_product, list_product, add_batch, list_batch, add_bill, list_bill, bill_detail
from variables import ENTRY_FONT, TABLE_HEADER_FONT, TABLE_DATA_FONT


# -------------------------------------- Main Window -------------------------------------- #
root = tk.Tk()
root.title("Item Manager")
root.state("zoomed")
frame = ttk.Frame(root)
frame.pack(expand=True, fill="both")
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
# ----------------------------------------------------------------------------------------- #


# ----------------------------------------- Style ----------------------------------------- #
style = ttk.Style(root)
style.configure("Treeview", font=TABLE_DATA_FONT)
style.configure("Treeview.Heading", font=TABLE_HEADER_FONT)
# ----------------------------------------------------------------------------------------- #


# ----------------------------------------- Pages ----------------------------------------- #
addProduct = add_product.Frame(frame)
listProduct = list_product.Frame(frame)
addBatch = add_batch.Frame(frame)
listBatch = list_batch.Frame(frame)
addBill = add_bill.Frame(frame)
billDetail = bill_detail.Frame(frame)
listBill = list_bill.Frame(frame, billDetail)
# ----------------------------------------------------------------------------------------- #


# ---------------------------------------- MenuBar ---------------------------------------- #
menubar = tk.Menu(root)

product_menu = tk.Menu(menubar, tearoff=0)
product_menu.add_command(label="New Item", command=addProduct.set_active)
product_menu.add_command(label="List Item", command=listProduct.set_active)
product_menu.add_separator()
product_menu.add_command(label="New Batch", command=addBatch.set_active)
product_menu.add_command(label="List Batch", command=listBatch.set_active)

bill_menu = tk.Menu(menubar, tearoff=0)
bill_menu.add_command(label="New Bill", command=addBill.set_active)
bill_menu.add_command(label="List Bill", command=listBill.set_active)

menubar.add_cascade(label="Item", menu=product_menu)
menubar.add_cascade(label="Bill", menu=bill_menu)
root.config(menu=menubar)
# ----------------------------------------------------------------------------------------- #


root.option_add("*TCombobox*Listbox*Font", ENTRY_FONT)
addProduct.set_active()


def start() -> None:
    root.mainloop()
