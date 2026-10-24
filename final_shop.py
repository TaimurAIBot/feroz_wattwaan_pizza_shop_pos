import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os, tempfile

LOCK_FILE = ".views_count.txt"
views = 0
if os.path.exists(LOCK_FILE):
    try:
        with open(LOCK_FILE, "r") as f:
            views = int(f.read())
    except:
        views = 0
views += 1
with open(LOCK_FILE, "w") as f:
    f.write(str(views))
if views > 5:
    r = tk.Tk(); r.withdraw()
    messagebox.showerror("🔒 DEMO KHATAM", "Demo 5 bar khatam!\nContact: Taimur Wattoo\n03020700310\ntaimurwattoo.ai@gmail.com")
    r.destroy(); exit()

MENU = {"Small Pizza":450,"Medium Pizza":850,"Large Pizza":1250,"Zinger Burger":350,"Zinger Cheese Burger":420,"Chicken Burger":300,"Beef Burger":380,"Hot Wings 6 Pcs":500,"Hot Wings 12 Pcs":950,"French Fries Small":150,"French Fries Large":250,"Loaded Fries":400,"Chicken Shawarma":250,"Zinger Shawarma":320,"Chicken Pasta":450,"Cold Drink Small":80,"Cold Drink Large":150,"Ice Cream Scoop":120,"Garlic Bread":200,"Potato Wedges":280}
cart={}; last_slip=""
root=tk.Tk(); root.title(f"Pizza Shop PRO | Demo {views}/5 | 03020700310"); root.geometry("1150x720")
top=tk.Frame(root, bg="#ff9800", pady=10); top.pack(fill="x"); tk.Label(top, text=f"🍕 FEROZ WATTWAAN PIZZA | Demo {views}/5 | Taimur: 03020700310", bg="#ff9800", fg="white", font=("Arial",11,"bold")).pack()
cf=tk.Frame(root,pady=10); cf.pack(fill="x"); tk.Label(cf,text="Customer Naam:",font=("Arial",12,"bold")).pack(side="left",padx=10); name_entry=tk.Entry(cf,width=15); name_entry.pack(side="left"); tk.Label(cf,text="Phone:").pack(side="left",padx=10); phone_entry=tk.Entry(cf,width=12); phone_entry.pack(side="left")
main=tk.Frame(root); main.pack(fill="both",expand=True,padx=10); left=tk.Frame(main); left.pack(side="left",fill="both",expand=True); right=tk.Frame(main,bg="#f5f5f5",width=420,bd=2,relief="ridge"); right.pack(side="right",fill="y",padx=5)
sf=tk.Frame(left); sf.pack(fill="x",pady=5); tk.Label(sf,text="🔍 Price Likho:").pack(side="left"); search_entry=tk.Entry(sf,width=25); search_entry.pack(side="left",padx=5)
canvas=tk.Canvas(left); scroll=tk.Scrollbar(left,orient="vertical",command=canvas.yview); scrollable=tk.Frame(canvas); scrollable.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all"))); canvas.create_window((0,0),window=scrollable,anchor="nw"); canvas.configure(yscrollcommand=scroll.set); canvas.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y")
def render_items(ft=""):
    for w in scrollable.winfo_children(): w.destroy()
    for item,price in MENU.items():
        if ft.lower() in item.lower():
            row=tk.Frame(scrollable,pady=4,bg="white",bd=1,relief="solid"); row.pack(fill="x",padx=5,pady=2)
            tk.Label(row,text=item,width=22,anchor="w",bg="white",font=("Arial",10,"bold")).pack(side="left",padx=5); tk.Label(row,text=f"Rs.{price}",width=8,bg="white",fg="green",font=("Arial",10,"bold")).pack(side="left")
            tk.Label(row,text=f"Qty:{cart.get(item,0)}",width=7).pack(side="left"); tk.Button(row,text="➕",bg="#4caf50",fg="white",command=lambda i=item:add_item(i)).pack(side="left",padx=3); tk.Button(row,text="➖",bg="#f44336",fg="white",command=lambda i=item:sub_item(i)).pack(side="left",padx=3)
def add_item(item): cart[item]=cart.get(item,0)+1; update_bill()
def sub_item(item):
    if cart.get(item,0)>0:
        cart[item]-=1
        if cart[item]==0: del cart[item]
        update_bill()
def update_bill():
    render_items(search_entry.get()); total_items=sum(cart.values()); total_bill=sum([MENU[k]*v for k,v in cart.items()]); bill_text.set(f"Total Items: {total_items}\nTotal Bill: Rs.{total_bill}"); detail_box.delete(1.0,tk.END)
    for k,v in cart.items(): detail_box.insert(tk.END,f"{k} x {v} = Rs.{MENU[k]*v}\n")
tk.Label(right,text="🔔 FINAL BILL",font=("Arial",15,"bold"),bg="#f5f5f5").pack(pady=8); bill_text=tk.StringVar(value="Total Items: 0\nTotal Bill: Rs.0"); tk.Label(right,textvariable=bill_text,font=("Arial",14,"bold"),bg="#f5f5f5",fg="#2e7d32").pack(); detail_box=tk.Text(right,height=12,font=("Arial",10)); detail_box.pack(fill="x",padx=10,pady=5)
tk.Label(right,text="💰 Udhar Hai?",bg="#f5f5f5",font=("Arial",11,"bold")).pack(pady=5); pay_var=tk.StringVar(value="Full Paid"); fp=tk.Frame(right,bg="#f5f5f5"); fp.pack(); tk.Radiobutton(fp,text="Full Paid",variable=pay_var,value="Full Paid",bg="#f5f5f5").pack(side="left"); tk.Radiobutton(fp,text="Full Udhar",variable=pay_var,value="Full Udhar",bg="#f5f5f5",fg="red").pack(side="left"); tk.Radiobutton(fp,text="Half",variable=pay_var,value="Half Paid",bg="#f5f5f5").pack(side="left")
tk.Label(right,text="Custom Paid Kitna?",bg="#f5f5f5",font=("Arial",9)).pack(); custom_paid_entry=tk.Entry(right,width=15); custom_paid_entry.pack()
def final_bill_process():
    global last_slip; name=name_entry.get(); phone=phone_entry.get()
    if not name: messagebox.showwarning("Naam?","Naam likho!"); return
    total_bill=sum([MENU[k]*v for k,v in cart.items()])
    if total_bill==0: messagebox.showwarning("Khali","Item lo!"); return
    paid=total_bill; ptype=pay_var.get()
    if ptype=="Half Paid": paid=total_bill//2
    elif ptype=="Full Udhar": paid=0
    if custom_paid_entry.get()!="":
        try: paid=int(custom_paid_entry.get())
        except: pass
    udhar=total_bill-paid
    last_slip=f"FEROZ WATTWAAN PIZZA - Dev Taimur 03020700310\nCustomer: {name}\nPhone: {phone}\nDate: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n----------------\n"
    for k,v in cart.items(): last_slip+=f"{k} x {v} = Rs.{MENU[k]*v}\n"
    last_slip+=f"----------------\nTotal: Rs.{total_bill}\nPaid: Rs.{paid}\nUdhar: Rs.{udhar}\nThanks!\n"
    with open("customers.txt","a",encoding="utf-8") as f: f.write(last_slip.replace("\n"," | ")+"\n")
    nd={"Date":datetime.now(),"Name":name,"Phone":phone,"Total":total_bill,"Paid":paid,"Udhar":udhar,"Items":str(list(cart.keys()))}
    if os.path.exists("customers.xlsx"): old=pd.read_excel("customers.xlsx"); new_df=pd.concat([old,pd.DataFrame([nd])],ignore_index=True)
    else: new_df=pd.DataFrame([nd])
    new_df.to_excel("customers.xlsx",index=False); messagebox.showinfo("Bill Ready",last_slip+"\nSave Ho Gaya! PRINT dabao!")
def print_bill():
    if last_slip=="": messagebox.showwarning("Pehle Bill Banao","Pehle BILL BANA DO!"); return
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=".txt",mode="w",encoding="utf-8") as f: f.write(last_slip); tn=f.name
        os.startfile(tn,"print"); messagebox.showinfo("Print","🖨️ Bill Printer Par Gaya!")
    except:
        with open(f"Bill_{name_entry.get()}.txt","w",encoding="utf-8") as f: f.write(last_slip)
        messagebox.showinfo("Print",f"Bill file: Bill_{name_entry.get()}.txt")
def total_sales_show():
    if os.path.exists("customers.xlsx"): df=pd.read_excel("customers.xlsx"); messagebox.showinfo("💰 Sale",f"Total Sale: Rs.{df['Total'].sum()}\nPaid: Rs.{df['Paid'].sum()}\nUdhar: Rs.{df['Udhar'].sum()}")
    else: messagebox.showinfo("Sale","Koi sale nahi!")
def udhar_list_show():
    if os.path.exists("customers.xlsx"): df=pd.read_excel("customers.xlsx"); udf=df[df["Udhar"]>0]; 
    else: messagebox.showinfo("Udhar","Koi Data Nahi!"); return
    if len(udf)>0: messagebox.showinfo("📒 Udhar",udf[["Name","Phone","Udhar"]].to_string())
    else: messagebox.showinfo("Udhar","Koi Udhar Nahi!")
tk.Button(right,text="🔔 BILL BANA DO",bg="#1565c0",fg="white",font=("Arial",11,"bold"),command=final_bill_process,height=2).pack(fill="x",padx=10,pady=5); tk.Button(right,text="🖨️ PRINT",bg="#2e7d32",fg="white",font=("Arial",11,"bold"),command=print_bill,height=2).pack(fill="x",padx=10,pady=5)
f2=tk.Frame(right,bg="#f5f5f5"); f2.pack(fill="x",pady=10); tk.Button(f2,text="💰 Total Sale",bg="#ff9800",fg="white",font=("Arial",10,"bold"),command=total_sales_show).pack(side="left",expand=True,padx=5); tk.Button(f2,text="📒 Udhar List",bg="#e91e63",fg="white",font=("Arial",10,"bold"),command=udhar_list_show).pack(side="left",expand=True,padx=5)
search_entry.bind("<KeyRelease>",lambda e:render_items(search_entry.get())); render_items(); root.mainloop()