import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("JilvianX")
root.geometry("500x400")

def show_products():
    messagebox.showinfo("Produk", "Daftar produk akan tampil di sini")

title = tk.Label(
    root,
    text="JilvianX Future Vending Machine",
    font=("Arial", 16, "bold")
)
title.pack(pady=20)

btn_product = tk.Button(
    root,
    text="Product Catalog",
    width=25,
    command=show_products
)
btn_product.pack(pady=10)

root.mainloop()