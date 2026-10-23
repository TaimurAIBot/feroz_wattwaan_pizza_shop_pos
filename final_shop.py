# Feroz Wattwaan Pizza Shop - POS System
# Developed by Taimur Al-Bot

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

root = tk.Tk()
root.title("Feroz Wattwaan Pizza Shop POS - By Taimur")
root.geometry("800x550")
root.configure(bg="#FFF8E7")

tk.Label(root, text="Feroz Wattwaan Pizza Shop", font=("Arial", 20, "bold"), bg="#FFF8E7", fg="#D32F2F").pack(pady=10)
tk.Label(root, text="Arifwala Road, Sahiwal | POS v1.0", font=("Arial", 10), bg="#FFF8E7").pack()

items = {"Chicken Tikka Small": 800, "Chicken Tikka Large": 1500, "Fajita Small": 850, "Fajita Large": 1600, "Cold Drink": 150, "Fries": 250}
vars_dict = {}

frame = tk.Frame(root, bg="white")
frame.pack(pady=10, padx=20, fill="x")

for item, price in items.items():
    v = tk.IntVar()
    tk.Checkbutton(frame, text=f"{item} - Rs.{price}", variable=v, bg="white").pack(anchor="w", padx=10)
    vars_dict[item] = v

bill_text = tk.Text(root, height=10, width=80)
bill_text.pack(pady=10)

def gen_bill():
    total=0
    bill=f"--- Bill ---\n{datetime.now()}\n"
    for i,v in vars_dict.items():
        if v.get()==1:
            bill+=f"{i} : {items[i]}\n"
            total+=items[i]
    if total==0:
        messagebox.showwarning("Error","Select item")
        return
    bill+=f"TOTAL: Rs.{total}\nThanks - Taimur"
    bill_text.delete("1.0", tk.END)
    bill_text.insert(tk.END, bill)

tk.Button(root, text="Generate Bill", command=gen_bill, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
root.mainloop()
