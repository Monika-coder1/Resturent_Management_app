from tkinter import *
from tkinter import messagebox
import mysql.connector as sql

# === Step 1: Connect to MySQL (initial connection without DB to create one) ===
try:
    db_init = sql.connect(
        host="localhost",
        user="root",
        password="@123"
    )
    cr_init = db_init.cursor()
    cr_init.execute("CREATE DATABASE IF NOT EXISTS resturent_management_db")
    db_init.commit()
    db_init.close()
except sql.Error as err:
    print("Database creation failed:", err)
    exit()

# === Step 2: Connect to the actual DB ===
try:
    db = sql.connect(
        host="localhost",
        user="root",
        password="@123",
        database="resturent_management_db",
        use_pure=True
    )
    cr = db.cursor()

    # === Step 3: Create orders table if not exists ===
    cr.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(15),
            order_date DATE,
            items TEXT,
            total_price INT
        )
    """)
    db.commit()
except sql.Error as err:
    print("Final DB connection failed:", err)
    exit()

# === Tkinter GUI Setup ===
df = Tk()
df.title("Hariom Restaurant Management App")
df.geometry("1200x720")
df.configure(bg="#f4f4f4")

# === Top Frame ===
top_frame = Frame(df, bg="#e63946", height=100)
top_frame.pack(fill=X)
Label(top_frame, text="Hariom Restaurant", font=("Verdana", 28, "bold"), bg="#e63946", fg="white").pack(pady=20)

# === Center Logo ===
try:
    img1 = PhotoImage(file="C:/Users/Lenovo/Downloads/ompg.png")
    img_label = Label(df, image=img1, bg="#f4f4f4")
    img_label.place(x=480, y=120)
except Exception as e:
    print("Image not found or invalid:", e)

# === Input Variables ===
name_var = StringVar()
email_var = StringVar()
phone_var = StringVar()

menu_items = {
    "Paneer Butter Masala": 150,
    "Veg Biryani": 120,
    "Tandoori Roti": 20,
    "Butter Naan": 30,
    "Cold Drink": 40
}
item_vars = {}

# === Left Frame: Menu ===
menu_frame = LabelFrame(df, text="🍽️ Menu", font=("Arial", 14, "bold"),
                        bg="#fff0db", padx=20, pady=10, bd=3, relief=RIDGE)
menu_frame.place(x=50, y=300, width=350, height=330)

y_pos = 0
for item, price in menu_items.items():
    var = IntVar()
    item_vars[item] = var
    Checkbutton(menu_frame, text=f"{item} - ₹{price}", variable=var,
                bg="#fff0db", font=("Arial", 12)).grid(row=y_pos, column=0, sticky="w", pady=5)
    y_pos += 1

# === Right Frame: Registration Form ===
form_frame = LabelFrame(df, text="🧾 Customer Details", font=("Arial", 14, "bold"),
                        bg="#d0f4de", padx=20, pady=10, bd=3, relief=RIDGE)
form_frame.place(x=750, y=300, width=380, height=260)

Label(form_frame, text="Name:", bg="#d0f4de", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
Entry(form_frame, textvariable=name_var, width=25).grid(row=0, column=1, pady=5, padx=10)

Label(form_frame, text="Email:", bg="#d0f4de", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
Entry(form_frame, textvariable=email_var, width=25).grid(row=1, column=1, pady=5, padx=10)

Label(form_frame, text="Phone:", bg="#d0f4de", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
Entry(form_frame, textvariable=phone_var, width=25).grid(row=2, column=1, pady=5, padx=10)

# === Submit Function ===
def sub():
    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    selected_items = [item for item, var in item_vars.items() if var.get() == 1]
    items_str = ", ".join(selected_items)
    total_price = sum(menu_items[item] for item in selected_items)

    if not (name and email and phone and selected_items):
        messagebox.showwarning("Incomplete", "Please fill all fields and select at least one item.")
        return

    try:
        cr.execute("""
            INSERT INTO orders (name, email, phone, order_date, items, total_price)
            VALUES (%s, %s, %s, CURDATE(), %s, %s)
        """, (name, email, phone, items_str, total_price))
        db.commit()

        messagebox.showinfo("Congratulations!", f"🎉 Order placed successfully!\nTotal: ₹{total_price}")
        result_label.config(text=f"🎉 Order placed! Total: ₹{total_price}")
        df.after(4000, lambda: result_label.config(text=""))

        name_var.set("")
        email_var.set("")
        phone_var.set("")
        for var in item_vars.values():
            var.set(0)

    except sql.Error as err:
        messagebox.showerror("Database Error", str(err))

# === Submit Button ===
Button(df, text="✅ Submit Order", font=("Arial", 14, "bold"), bg="#06d6a0", fg="white",
       width=20, command=sub).place(x=800, y=580)

# === Result Message ===
result_label = Label(df, text="", font=("Arial", 14, "bold"), fg="green", bg="#f4f4f4")
result_label.place(x=470, y=670)

df.mainloop()