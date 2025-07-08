from tkinter import *
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from billing import BillClass
import sqlite3
import os
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x800+0+0")
        self.root.title("Billing menagement |  dev by amit")
        self.root.config(bg="black")


          # ===== Load and Resize Background Image =====
        self.bg_image = Image.open("images/headway-5QgIuuBxKwM-unsplash.jpg")  # Load image
        self.bg_image = self.bg_image.resize((1850, 1200), Image.LANCZOS)  # Resize to window size
        self.bg_image = self.bg_image.filter(ImageFilter.GaussianBlur(radius=0))  # Apply Blur
        self.bg_image = ImageTk.PhotoImage(self.bg_image)  # Convert for Tkinter

        # Create a Label for Background (Full Screen)
        self.bg_label = Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover Full Screen








        self.icon_title=PhotoImage(file="images/IUc8ohx-nsXP3sK.png")
        title=Label(self.root,text="Inventory  Management System ",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #logout button 
        btn_logout=Button(self.root,text="logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand").place(x=1100,y=25,height=30,width=150)

        #====clock====
        self.lbl_clock_=Label(self.root,text="welcome to inventary management system\t\t date: DD-MM-YYYY\t\t Time: HH:MM:SS ",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock_.place(x=0,y=70,relwidth=1,height=30)
       
        #==left menu==
        self.MenuLogo=Image.open("images/CS0PXMQM8ocyn33.png")
        self.MenuLogo=self.MenuLogo.resize((200,200))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=620)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        #this code for feame icon image code
        self.icon_side=Image.open("images/fast-forward.png")
        self.icon_side=self.icon_side.resize((20,20))
        self.icon_side=ImageTk.PhotoImage(self.icon_side)

        #menu and frame buttons 
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)

        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=10,cursor="hand").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=10,cursor="hand").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=10,cursor="hand").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="product",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=10,cursor="hand").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=10,cursor="hand").pack(side=TOP,fill=X)
        btn_billing=Button(LeftMenu,text="billing",command=self.billing,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=10,cursor="hand").pack(side=TOP,fill=X)

        btn_exit=Button(LeftMenu,text="exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=15,cursor="hand").pack(side=TOP,fill=X)



        #content
        self.lbl_employee=Label(self.root,text="total employee\n[ 0 ]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style ",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="total supplier\n[ 0 ]",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style ",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="total category\n[ 0 ]",bd=5,relief=RIDGE,bg="#009668",fg="white",font=("goudy old style ",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="total product\n[ 0 ]",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style ",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="total sales\n[ 0 ]",bd=5,relief=RIDGE,bg="purple",fg="white",font=("goudy old style ",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        # self.lbl_billing=Label(self.root,text="total billing\n[ 0 ]",bd=5,relief=RIDGE,bg="purple",fg="white",font=("goudy old style ",20,"bold"))
        # self.lbl_billing.place(x=650,y=300,height=150,width=300)



        #==footer==
       

        lbl_footer_=Label(self.root,text="IMS-Inventory management system |devloped by amit\n For any Technical issue contact:8875910376",font=("times new roman",12),bg="black",fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def billing(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=BillClass(self.new_win)
    
    def update_content(self):
         
         con=sqlite3.connect(database=r'ims.db')
         cur=con.cursor()
         try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'total products\n[{str(len(product))}]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'total supplier\n[{str(len(supplier))}]')
            

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'total category\n[{str(len(category))}]')


            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'total employee\n[{str(len(employee))}]')

            #sales part deskboard
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales [{str(bill)}]')

         except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)


if __name__=="__main__":

    root=Tk()
    obj= IMS(root)
    root.mainloop()

