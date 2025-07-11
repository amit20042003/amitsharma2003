from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+200+130")
        self.root.title("Inventory menagement |  dev by amit")
        self.root.config(bg="white")
        self.root.focus_force()
        #==========================
        #All variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar() 


        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        
       
        
        
        #===searchFrame===

        #options search employee(combo box)
        lbl_search=Label(self.root,text="Invoice no",font=("goudy old style",15),bg="white",fg="black")
        lbl_search.place(x=700,y=80)

        #search button
        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="white").place(x=800,y=80,width=160)
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15),bg="white",cursor="hand").place(x=980,y=80,width=100,height=28)

        #show all button
        btn_show_all = Button(self.root, text="Show All", command=self.show_all, font=("goudy old style", 15), bg="gray", cursor="hand2").place(x=570, y=9, width=150, height=30)


        #title
        title=Label(self.root,text="Supplier detials",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40),Pack()


        #content
        #====row1===#
        lbl_supplier_invoice=Label(self.root,text="Invoice no.",font=("goudy old style",15),bg="white").place(x=50,y=80)
        #this is for input box
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="white").place(x=150,y=80,width=180)
        
        
        #====row2===#
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="white").place(x=150,y=120,width=180)
        
        #===row3===#
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="white").place(x=150,y=160,width=180)
        


        #===row4===#
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=200)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="white")
        self.txt_desc.place(x=150,y=200,width=470,height=120)


        #===buttons===#

        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),cursor="hand2").place(x=150,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),cursor="hand2").place(x=280,y=370,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),cursor="hand2").place(x=400,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),cursor="hand2").place(x=520,y=370,width=110,height=35)


        #employee detials:
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=350)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Invoice No.")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="contact")
        self.supplierTable.heading("desc",text="desc")
        
        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
        self.supplierTable.pack(fill=BOTH,expand=1)
        
        #getting data from table and show the data in gui function
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
    #====================================================================

    def add(self):
     con=sqlite3.connect(database=r'ims.db')
     cur=con.cursor()
     try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice number  already assigned,try different",parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                                self.var_sup_invoice.get(),
                                self.var_name.get(),
                                self.var_contact.get(),
                                self.txt_desc.get('1.0',END),
                                
                    ))
                    con.commit()
                    messagebox.showinfo("success","Supplier added successfully",parent=self.root)
                    self.show()
     except Exception as ex:
        messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)




    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)

    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        # print(row)
        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert('1.0',row[3])
        

    #update function 
    def update(self): 
     con=sqlite3.connect(database=r'ims.db')
     cur=con.cursor()
     try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","INVOICE NO must be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                                
                                self.var_name.get(),                            
                                self.var_contact.get(),
                                self.txt_desc.get('1.0',END),
                                self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("success","Supplier Updated  successfully",parent=self.root)
                    self.show()
     except Exception as ex:
        messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)
   
    #delete function 
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice no  must be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid invoice no",parent=self.root)
                else:
                    op=messagebox.askyesno("conform","do you really want to delete",parent=self.root)
                    if op==True:
                     cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                     con.commit()
                    messagebox.showinfo("Delete","Supplier deleted successfully",parent=self.root)
                    # self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)


    def clear(self):
        self.var_sup_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),
        self.txt_desc.delete('1.0',END),
        self.var_searchtxt.set(""),
        self.show()
    

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice no should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row != None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    
    def show_all(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            if rows:
                for row in rows:
                    self.supplierTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No data found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()


    
if __name__=="__main__": 

    root=Tk()
    obj=supplierClass(root)
    root.mainloop()