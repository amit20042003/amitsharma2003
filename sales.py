from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os


class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+200+130")
        self.root.title("Inventory Management | Developed by Amit")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_invoice = StringVar()

        # Title
        lbl_title = Label(self.root, text="View Customer Bills", font=("goudy old style", 30), bg="#184a45", fg="white")
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

        # Invoice Input
        lbl_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white")
        lbl_invoice.place(x=50, y=100)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), bg="white")
        txt_invoice.place(x=160, y=100, width=180, height=28)

        # Buttons
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"),cursor="hand", command=self.search_invoice)
        btn_search.place(x=360, y=100, width=120, height=28)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"),cursor="hand", command=self.clear_fields)
        btn_clear.place(x=490, y=100, width=120, height=28)
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"),cursor="hand", command=self.delete_invoice)
        btn_delete.place(x=620, y=100, width=120, height=28)

        # Bill List
        sales_Frame = Frame(self.root, bg="white")
        sales_Frame.place(x=5, y=140, width=250, height=330)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.bill_list = Listbox(sales_Frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.bill_list.yview)
        self.bill_list.pack(fill=BOTH, expand=1)

        self.bill_list.bind("<Double-Button-1>", self.get_invoice_data)

        # Bill Area
        bill_Frame = Frame(self.root, bg="white", relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)

        lbl_title2 = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 20), bg="orange")
        lbl_title2.pack(side=TOP, fill=X, padx=10, pady=20)

        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg="white", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # Image Adjustment (Updated for better placement and scaling)
        self.bill_photo = Image.open("images/bill_12691170.png")

        # Resize the image to fit the remaining space without stretching
        self.bill_photo = self.bill_photo.resize((450, 300), Image.Resampling.LANCZOS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        # Create a label for the image and place it properly
        lbl_image = Label(self.root, image=self.bill_photo,bd=0)
        lbl_image.place(x=700, y=180, width=350, height=300)  # Adjust size and position based on your layout


    ######################################################

    def show(self):
        self.Sal




        # Initialize Database and Populate Dummy Data
        self.init_database()
        self.show_all_invoices()

    def init_database(self):
        """Initialize the database and populate it with dummy data."""
        con = sqlite3.connect("inventory.db")
        cur = con.cursor()
        # Create Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_no TEXT PRIMARY KEY,
            customer_name TEXT,
            bill_details TEXT
        )
        """)
        # Insert Dummy Data
        cur.execute("INSERT OR IGNORE INTO invoices VALUES ('INV001', 'John Doe', 'Product A: 2 pcs\nProduct B: 3 pcs\nTotal: $200')")
        cur.execute("INSERT OR IGNORE INTO invoices VALUES ('INV002', 'Jane Smith', 'Product C: 1 pcs\nProduct D: 4 pcs\nTotal: $150')")
        cur.execute("INSERT OR IGNORE INTO invoices VALUES ('INV003', 'Alice Brown', 'Product E: 5 pcs\nTotal: $300')")
        con.commit()
        con.close()

    def show_all_invoices(self):
        """Fetch all invoices from the database and display them in the list."""
        self.bill_list.delete(0, END)
        con = sqlite3.connect("inventory.db")
        cur = con.cursor()
        cur.execute("SELECT invoice_no FROM invoices")
        invoices = cur.fetchall()
        for inv in invoices:
            self.bill_list.insert(END, inv[0])
        con.close()

    def search_invoice(self):
        """Search for a specific invoice by invoice number."""
        invoice_no = self.var_invoice.get()
        if invoice_no == "":
            messagebox.showerror("Error", "Invoice number is required!", parent=self.root)
            return

        self.bill_area.delete("1.0", END)
        con = sqlite3.connect("inventory.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM invoices WHERE invoice_no=?", (invoice_no,))
        invoice = cur.fetchone()
        con.close()

        if invoice:
            self.bill_area.insert(END, f"Invoice No: {invoice[0]}\n")
            self.bill_area.insert(END, f"Customer Name: {invoice[1]}\n")
            self.bill_area.insert(END, f"Details:\n{invoice[2]}")
        else:
            messagebox.showerror("Error", "Invoice not found!", parent=self.root)

    def get_invoice_data(self, event):
        """Display selected invoice details in the bill area."""
        selected_invoice = self.bill_list.get(self.bill_list.curselection())
        self.var_invoice.set(selected_invoice)
        self.search_invoice()

    def delete_invoice(self):
        """Delete a selected invoice."""
        invoice_no = self.var_invoice.get()
        if invoice_no == "":
            messagebox.showerror("Error", "Please select an invoice to delete!", parent=self.root)
            return

        con = sqlite3.connect("inventory.db")
        cur = con.cursor()
        cur.execute("DELETE FROM invoices WHERE invoice_no=?", (invoice_no,))
        con.commit()
        con.close()
        self.show_all_invoices()
        self.clear_fields()
        messagebox.showinfo("Success", "Invoice deleted successfully!", parent=self.root)

    def clear_fields(self):
        """Clear all input fields and text areas."""
        self.var_invoice.set("")
        self.bill_area.delete("1.0", END)


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
