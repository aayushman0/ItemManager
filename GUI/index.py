import tkinter as tk
from tkinter import ttk
from GUI.pages import general  # , import_db
from GUI.pages import add_product, list_product, product_detail
from GUI.pages import add_batch, list_batch, batch_detail
from GUI.pages import add_bill, list_bill, bill_detail
from GUI.pages import add_service_bill, list_service_bill, service_bill_detail
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
productDetail = product_detail.Frame(frame)
listProduct = list_product.Frame(frame, productDetail)

addBatch = add_batch.Frame(frame)
batchDetail = batch_detail.Frame(frame)
listBatch = list_batch.Frame(frame, batchDetail)

addBill = add_bill.Frame(frame)
billDetail = bill_detail.Frame(frame)
listBill = list_bill.Frame(frame, billDetail)

addServiceBill = add_service_bill.Frame(frame)
serviceBillDetail = service_bill_detail.Frame(frame)
listServiceBill = list_service_bill.Frame(frame, serviceBillDetail)

generalPage = general.Frame(frame, productDetail, batchDetail, billDetail)
# importPage = import_db.Frame(frame)
# ----------------------------------------------------------------------------------------- #


# ---------------------------------------- MenuBar ---------------------------------------- #
menubar = tk.Menu(root)

general_menu = tk.Menu(menubar, tearoff=0)
general_menu.add_command(label="Index", command=generalPage.set_active)

product_menu = tk.Menu(menubar, tearoff=0)
product_menu.add_command(label="New Item", command=addProduct.set_active)
product_menu.add_command(label="List Item", command=listProduct.set_active)
product_menu.add_separator()
product_menu.add_command(label="New Batch", command=addBatch.set_active)
product_menu.add_command(label="List Batch", command=listBatch.set_active)

bill_menu = tk.Menu(menubar, tearoff=0)
bill_menu.add_command(label="New Bill", command=addBill.set_active)
bill_menu.add_command(label="List Bill", command=listBill.set_active)

service_bill_menu = tk.Menu(menubar, tearoff=0)
service_bill_menu.add_command(label="New Service Bill", command=addServiceBill.set_active)
service_bill_menu.add_command(label="List Service Bill", command=listServiceBill.set_active)

# extra_menu = tk.Menu(menubar, tearoff=0)
# extra_menu.add_command(label="Import", command=importPage.set_active)

menubar.add_cascade(label="   General  ", menu=general_menu)
menubar.add_cascade(label="   Item     ", menu=product_menu)
menubar.add_cascade(label="   Bill     ", menu=bill_menu)
menubar.add_cascade(label="Service Bill", menu=service_bill_menu)
# menubar.add_cascade(label="   Extra    ", menu=extra_menu)

root.config(menu=menubar)
# ----------------------------------------------------------------------------------------- #


root.option_add("*TCombobox*Listbox*Font", ENTRY_FONT)
generalPage.set_active()


def start() -> None:
    root.mainloop()
