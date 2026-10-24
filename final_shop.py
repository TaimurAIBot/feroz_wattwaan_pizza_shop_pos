import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# ===== FILES =====
LOCK_FILE = ".views_count.txt"
SALES_FILE = ".total_sales.txt"
UDHAR_FILE = ".udhar_list.txt"
MAX_TRIAL = 5

def check_trial():
    count = 0
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                count = int(f.read().strip())
        except:
            count = 0
    count += 1
    with open(LOCK_FILE, "w") as f:
        f.write(str(count))
    if count > MAX_TRIAL:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("DEMO KHATAM", "Demo 5 bar khatam!\n\nContact Taimur Wattoo\n03020700310\ntaimurwattoo.ai@gmail.com\n\nFull Version ke liye rabta karein!")
        root.destroy()
        exit()
    return count

def get_total_sales():
    if os.path.exists(SALES_FILE):
        try:
            with open(SALES_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def add_sales(amount):
    total = get_total_sales() + amount
    with open(SALES_FILE, "w") as f:
        f.write(str(total))

def save_udhar(name, amount):
    with open(UDHAR_FILE, "a") as f:
        f.write(f"{name} - Rs.{amount}\n")

def udhar_list_show():
    if not os.path.exists(UDHAR_FILE):
        messagebox.showinfo("Udhar List", "Koi Udhar nahi hai!")
        return
    try:
        with open(UDHAR_FILE, "r") as f:
            data = f.read()
        if not data.strip():
            messagebox.showinfo("Udhar List", "Koi Udhar nahi hai!")
        else:
            messagebox.showinfo("Udhar List - Taimur Wattoo", data)
    except:
        messagebox.showinfo("Udhar List", "Koi Udhar nahi hai!")

def total_sales_show():
    total = get_total_sales()
    messagebox.showinfo("Total Sales", f"Total Sale Till Now:\nRs. {total}\n\nDev: Taimur Wattoo\n03020700310")

views = check_trial()

# ===== MAIN APP =====
app = tk.Tk()
app.title(f"Pizza Shop PRO | Demo {views}/5 | 03020700310")
app.geometry("950x650")
app.configure(bg="#1a1a1a")

tk.Label(app, text="Feroz Wattwaan Pizza Shop", font=("Arial", 22, "bold"), bg="#1a1a1a", fg="#ffcc00").pack(pady=10)
tk.Label(app, text=f"PRO Version | Trial {views}/5 | Dev: Taimur Wattoo 03020700310", font=("Arial", 10), bg="#1a1a1a", fg="white").pack()

menu_frame = tk.Frame(app, bg="#2b2b2b")
menu_frame.pack(pady=15, padx=20, fill="both", expand=True)

menu_items = [
    ("Chicken Tikka Small", 450), ("Chicken Tikka Medium", 850),
    ("Chicken Tikka Large", 1250), ("Fajita Small", 500),
    ("Fajita Medium", 900), ("Fajita Large", 1300),
    ("Veg Burger", 250), ("Zinger Burger", 350),
]

cart = []
total = 0

def add_to_cart(name, price):
    global total
    cart.append((name, price))
    total += price
    cart_list.insert(tk.END, f"{name} - Rs.{price}")
    total_label.config(text=f"Total: Rs. {total}")

for i, (name, price) in enumerate(menu_items):
    tk.Button(menu_frame, text=f"{name} - Rs.{price}", command=lambda n=name, p=price: add_to_cart(n,p), bg="#ffcc00", fg="black", font=("Arial", 11, "bold"), width=26).grid(row=i//2, column=i%2, padx=10, pady=5)

cart_frame = tk.Frame(app, bg="#1a1a1a")
cart_frame.pack(pady=10, fill="both", padx=20)

tk.Label(cart_frame, text="Cart / Bill:", bg="#1a1a1a", fg="white", font=("Arial", 12, "bold")).pack(anchor="w")
cart_list = tk.Listbox(cart_frame, height=7, bg="white", font=("Arial", 11))
cart_list.pack(fill="both", pady=5)

total_label = tk.Label(cart_frame, text="Total: Rs. 0", bg="#1a1a1a", fg="#ffcc00", font=("Arial", 14, "bold"))
total_label.pack()

def clear_cart():
    global total
    cart.clear()
    total = 0
    cart_list.delete(0, tk.END)
    total_label.config(text="Total: Rs. 0")

def print_bill():
    global total
    if not cart:
        messagebox.showwarning("Empty", "Cart khali hai!")
        return
    bill = f"Feroz Wattwaan Pizza\n---\n"
    for n,p in cart:
        bill += f"{n} - Rs.{p}\n"
    bill += f"\nTotal: Rs.{total}\nThanks! - Taimur Wattoo 03020700310"
    add_sales(total)
    messagebox.showinfo("Bill", bill)
    clear_cart()

def add_udhar_entry():
    global total
    if not cart:
        messagebox.showwarning("Empty", "Cart khali hai!")
        return
    name = simpledialog.askstring("Udhar", "Customer ka naam likho:")
    if not name:
        return
    save_udhar(name, total)
    add_sales(total)
    messagebox.showinfo("Udhar", f"{name} ka Rs.{total} udhar save ho gaya!")
    clear_cart()

# ===== BUTTONS =====
btn_frame = tk.Frame(cart_frame, bg="#1a1a1a")
btn_frame.pack(pady=8)

tk.Button(btn_frame, text="Print Bill", command=print_bill, bg="green", fg="white", font=("Arial", 11, "bold"), width=14).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Clear Cart", command=clear_cart, bg="red", fg="white", font=("Arial", 11, "bold"), width=14).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Add Udhar", command=add_udhar_entry, bg="orange", fg="black", font=("Arial", 11, "bold"), width=14).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Udhar List", command=udhar_list_show, bg="#00bfff", fg="black", font=("Arial", 11, "bold"), width=14).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Total Sales", command=total_sales_show, bg="#ffcc00", fg="black", font=("Arial", 11, "bold"), width=14).grid(row=1, column=0, columnspan=2, pady=8, padx=5)
tk.Button(btn_frame, text="Exit", command=app.destroy, bg="gray", fg="white", font=("Arial", 11, "bold"), width=14).grid(row=1, column=2, columnspan=2, pady=8)

app.mainloop()