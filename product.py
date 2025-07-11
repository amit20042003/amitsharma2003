from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+200+130")
        self.root.title("Inventory menagement |  dev by amit")
        self.root.config(bg="white")
        self.root.focus_force()

        #All variables

        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.var_pid=StringVar() 

        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar() 




        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)
        #title
        title=Label(product_Frame,text="Manage Products detials",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_product_name=Label(product_Frame,text="prodct Name ",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_qty=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=310)

        
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=LEFT,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=LEFT,font=("goudy old style",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="white").place(x=150,y=160,width=200)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="white").place(x=150,y=210,width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="white").place(x=150,y=260,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("select","Active","inactive"),state='readonly',justify=LEFT,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        #buttons
        btn_add=Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15),cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),cursor="hand2").place(x=340,y=400,width=100,height=40)
            
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #options search employee(combo box)
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("select","Category","Supplier","Name"),state='readonly',justify=LEFT,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        #search button
        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="white").place(x=200,y=8)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="black",cursor="hand").place(x=410,y=9,width=150,height=30)
        #PRODUCT DETIALS
        #TREE VIEW
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.product_table=ttk.Treeview(p_frame,columns=("pid","Category","Supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.heading("pid",text="P id")
        self.product_table.heading("Category",text="Category")
        self.product_table.heading("Supplier",text="Supplier")
        self.product_table.heading("name",text="Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty",text="qty")
        self.product_table.heading("status",text="Status")

        self.product_table["show"]="headings"

        self.product_table.column("pid",width=90)
        self.product_table.column("Category",width=100)
        self.product_table.column("Supplier",width=100)
        self.product_table.column("name",width=100)
        self.product_table.column("price",width=100)
        self.product_table.column("qty",width=100)
        self.product_table.column("status",width=100)
    

        self.product_table.pack(fill=BOTH,expand=1)
        
        #getting data from table and show the data in gui function
        self.product_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        self.fetch_cat_sup()

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")

        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

            
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)


    def add(self):

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if (
                self.var_cat.get() == "Select" or
                self.var_sup.get() == "Select" or
                self.var_name.get().strip() == "" or
                self.var_price.get().strip() == "" or
                self.var_qty.get().strip() == "" or
                self.var_status.get() == "select"
            ):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already exists. Try a different name.", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO product (Category, Supplier, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()





    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)

    def get_data(self, ev):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content["values"]
        if row:
            self.var_pid.set(row[0])
            self.var_cat.set(row[1])
            self.var_sup.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])


    #update function 
    def update(self): 
     con=sqlite3.connect(database=r'ims.db')
     cur=con.cursor()
     try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","please select proguct from list ",parent=self.root)
            else:
                cur.execute("select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid product",parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(

                                
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("success","product Updated  successfully",parent=self.root)
                    self.show()
     except Exception as ex:
        messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)
   
    #delete function 
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select product from the list",parent=self.root)
            else:
                cur.execute("select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid product ",parent=self.root)
                else:
                    op=messagebox.askyesno("conform","do you really want to delete",parent=self.root)
                    if op==True:
                     cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                     con.commit()
                    messagebox.showinfo("Delete","Product deleted successfully",parent=self.root)
                    # self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)


    def clear(self):
        self.var_cat.set("Select"),
        self.var_sup.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set(""),
        self.var_pid.set("")
        
        self.var_searchtxt.set(""),
        self.var_searchby.set("select")
        self.show()
    

    def search(self):

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "select":
                messagebox.showerror("Error", "Select a search by option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                query = f"SELECT * FROM product WHERE {self.var_searchby.get()} LIKE ?"
                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if rows:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
if __name__=="__main__": 

    root=Tk()
    obj=productClass(root)
    root.mainloop()