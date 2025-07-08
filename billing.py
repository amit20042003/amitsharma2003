from tkinter import *
from tkinter import simpledialog
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os 
import tempfile
import subprocess
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title(" Billing menagement |  dev by amit")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        # Payment Info (new variables)
        self.var_payment_status = StringVar()  # Paid/Unpaid
        self.var_remaining_balance = DoubleVar()  # Remaining balance if any
        
        
        self.icon_title=PhotoImage(file="images/IUc8ohx-nsXP3sK.png")
        title=Label(self.root,text=" Food System ",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #logout button 
        btn_logout=Button(self.root,text="logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand").place(x=1100,y=25,height=30,width=150)

        #====clock====
        self.lbl_clock=Label(self.root,text="welcome to inventary management system\t\t date: DD-MM-YYYY\t\t Time: HH:MM:SS ",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)



    #===============%%%%%%%&&&&&&&======


     # === Payments Table Frame (🚀 New Code Added Here) ===
        self.payment_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.payment_frame.place(x=430, y=700, width=780, height=200)  # Position in middle

        # Update Payment Button (Placed Below the Payment Table)---->database
        self.btn_update_payment = Button(
            self.payment_frame, 
            text="Update Payment", 
            command=self.update_payment, 
            font=("Arial", 12, "bold"), 
            cursor="hand2"
        )
        self.btn_update_payment.pack(pady=5)  # Add padding below table

        # delete Payment Button (Placed Below the Payment Table)--->database
        self.btn_delete_payment = Button(
            self.payment_frame, 
            text="Delete Payment", 
            font=("Arial", 12, "bold"),
            cursor="hand2", 
            command=self.delete_payment
        )
        self.btn_delete_payment.place(x=500,y=5)



        # Scrollbars
        scroll_x = Scrollbar(self.payment_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.payment_frame, orient=VERTICAL)

        # Table
        self.PaymentTable = ttk.Treeview(
            self.payment_frame, 
            columns=("payment_id","bill_id", "amount_paid", "date", "remaining", "payment_type", "due_date"),
            xscrollcommand=scroll_x.set, 
            yscrollcommand=scroll_y.set
        )



        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.PaymentTable.xview)
        scroll_y.config(command=self.PaymentTable.yview)

        # Table Headings
        self.PaymentTable.heading("payment_id",text="payment_id")
        self.PaymentTable.heading("bill_id", text="Bill ID")
        self.PaymentTable.heading("amount_paid", text="Amount Paid")
        self.PaymentTable.heading("date", text="Payment Date")
        self.PaymentTable.heading("remaining", text="Remaining Balance")
        self.PaymentTable.heading("payment_type", text="Payment Type")
        self.PaymentTable.heading("due_date", text="Due Date")

        self.PaymentTable["show"] = "headings"

        # Column Width
        self.PaymentTable.column("payment_id", width=100)
        self.PaymentTable.column("bill_id", width=100)
        self.PaymentTable.column("amount_paid", width=100)
        self.PaymentTable.column("date", width=100)
        self.PaymentTable.column("remaining", width=120)
        self.PaymentTable.column("payment_type", width=100)
        self.PaymentTable.column("due_date", width=100)

        self.PaymentTable.pack(fill=BOTH, expand=1)






        self.load_payments()
        






    #==============%%%%%%%%%%%%%%+===========

        #=====product frame======#

                            

        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="All product",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
                     
                     
                        #Product Search  Frame ---------------#

        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By name ", font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=3,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15,"bold"),bg="lightYellow").place(x=110,y=47,width=150,height=22)

        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),cursor="hand").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show all",command=self.show,font=("goudy old style",15),cursor="hand").place(x=285,y=10,width=100,height=25)

                                    #Product Detials  Frame ---------------#

        
        ProductFrame3=Frame(self.root,bd=3,relief=RIDGE)
        ProductFrame3.place(x=9,y=250,width=400,height=385)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="qty")
        self.product_Table.heading("status",text="Status")

        
        self.product_Table["show"]="headings"

        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        #getting data from table and show the data in gui function
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",10),bg="white",fg="red").pack(side=BOTTOM,fill=X)



        #===========================Customer Frame =======================================
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=590,height=70)


        cTitle=Label(CustomerFrame,text="Customer Detials",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13,"bold"),bg="white").place(x=60,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No",font=("times new roman",15),bg="white").place(x=300,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13,"bold"),bg="white").place(x=380,y=35,width=140)

        #cal cart frame part ------------------:

        Cal_Cart_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=590,height=360)

                        #calculator Frame ---------------#
        self.var_cal_input=StringVar()
        Cal_Frame=Frame(Cal_Cart_Frame,bd=8,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=300,height=340)


        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=28,bd=10,relief=GROOVE,state="readonly",justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=3,pady=18,cursor="hand").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=3,pady=18,cursor="hand").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=3,pady=18,cursor="hand").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=3,pady=18,cursor="hand").grid(row=1,column=3)


        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=3,pady=18,cursor="hand").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=3,pady=18,cursor="hand").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=3,pady=18,cursor="hand").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=3,pady=18,cursor="hand").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=3,pady=18,cursor="hand").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=3,pady=18,cursor="hand").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=3,pady=18,cursor="hand").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=3,pady=18,cursor="hand").grid(row=3,column=3)


        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=3,pady=20,cursor="hand").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=3,pady=20,cursor="hand").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=3,pady=20,cursor="hand").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=3,pady=20,cursor="hand").grid(row=4,column=3)


   
 
        #----------add data left side table near calculator---------#
                # Cart Frame ---------------#

        cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=310,y=8,width=270,height=342)

        self.cartTitle=Label(cart_Frame,text="Cart \t Total product:[0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="qty")

        
        self.CartTable["show"]="headings"

        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=20)
        self.CartTable.pack(fill=BOTH,expand=1)
        #getting data from table and show the data in gui function
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #Add Cart Widgets Frame ---------------#
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()




        Add_cartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_cartWidgetsFrame.place(x=420,y=550,width=590,height=110)

        lbl_p_name=Label(Add_cartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_cartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_cartWidgetsFrame,text="Price per qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_cartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=120,height=22)

        lbl_p_qty=Label(Add_cartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=4)
        txt_p_qty=Entry(Add_cartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="white").place(x=390,y=33,width=100,height=22)

        self.lbl_instok=Label(Add_cartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instok.place(x=5,y=70)
        
        btn_clear_cart=Button(Add_cartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_cartWidgetsFrame,text="ADD | Update",command=self.add_update_cart,font=("times new roman",14,"bold"),bg="orange",cursor="hand").place(x=340,y=70,width=180,height=30)
        # btn_clear_cart=Button(Add_cartWidgetsFrame,text="Clear",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand").place(x=180,y=70,width=150,height=30)




        #=========== billing area================================
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=1010,y=110,width=510,height=430)

        BTitle=Label(billFrame,text="Customer bill area",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)



    


        #====billing buttons------->
        self.var_discount = StringVar()
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=1010,y=540,width=510,height=120)

        self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=("goudy old style",20,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=2,width=150,height=60)

        self.lbl_discount = Label(billMenuFrame, text="Enter Discount (%)", font=("times new roman", 15), bg="white")
        self.lbl_discount.place(x=180, y=0)  # Position the label on the screen

        self.ent_discount = Entry(billMenuFrame, textvariable=self.var_discount, font=("times new roman", 12 ,"bold"), bg="White")
        self.ent_discount.place(x=180, y=30, width=120, height=30)  

        self.lbl_net_pay=Label(billMenuFrame,text='Net Pay\n[0]',font=("goudy old style",20,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=326,y=2,width=160,height=60)







        btn_print=Button(billMenuFrame,text='Print',command=self.print_bill,cursor="hand",font=("goudy old style",20,"bold"))
        btn_print.place(x=2,y=80,width=120,height=37)

        btn_clear_all=Button(billMenuFrame,text='Clear All',command=self.clear_all,cursor="hand",font=("goudy old style",20,"bold"))
        btn_clear_all.place(x=169,y=80,width=120,height=37)

        btn_generate=Button(billMenuFrame,text='Generate Bill',command=self.generate_bill,cursor="hand",font=("goudy old style",20,"bold"))
        btn_generate.place(x=320,y=80,width=180,height=37)

        footer=Label(self.root,text="IMS-Inventory Management System | Devloped by Amit \n for any Tecnical issue contact: 8875XXXXXX",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.show()
        self.update_date_time()
        # self.bill_top()
    # all Functions=====>

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')
    
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)



    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                cur.execute("SELECT pid, name, price, qty, status FROM product WHERE name LIKE ? AND status = 'Active'", ('%' + self.var_search.get() + '%',))
                rows = cur.fetchall()
                if rows:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    



    def get_data(self, ev):
        f = self.product_Table.focus()
        content = self.product_Table.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instok.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self, ev):

        f = self.CartTable.focus()
        content = self.CartTable.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instok.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])
    
    def add_update_cart(self):
        if self.var_pid.get()=='':  
                        messagebox.showerror('Error',"please select product from the list ",parent=self.root)

        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity | Not Available check qty",parent=self.root)
        else:   
        #  price_cal=int(self.var_qty.get())*float(self.var_price.get())
        #  price_cal=float(price_cal)

            price_cal=self.var_price.get()
        #  pid,name,price,qty,status
        cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
        

        # update cart=======

        present='no'    
        index_=0
        for row in self.cart_list:
            if self.var_pid.get()==row[0]:
                present='yes'   
                break
            index_+=1
        
        if present =='yes':
            op=messagebox.askyesno('confirm',"Product already Present \n Do you want to Update | Remove from the Cart List",parent=self.root)
            if op==True:
                if self.var_qty.get()=="0":
                    self.cart_list.pop(index_)
                else:
                    # self.cart_list[index_][2]=price_cal #price
                    self.cart_list[index_][3]=self.var_qty.get()
        else:
            self.cart_list.append(cart_data)
        self.show_cart()
        self.bill_updates()



    def create_db(self):

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        # Create the payments table if it doesn't exist
        cur.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            bill_id INTEGER,
            amount_paid REAL,
            payment_date TEXT,
            remaining_balance REAL,
            payment_type TEXT,
            due_date TEXT
        );
        ''')
        con.commit()
        con.close()




    def bill_updates(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0

        # Calculate the total bill amount (sum of price * quantity for all products in cart)
        for row in self.cart_list:
            self.bill_amnt += float(row[2]) * int(row[3])  # Assuming row[2] is price and row[3] is quantity

        # Get the discount value entered by the user
        discount_input = self.var_discount.get()

        if discount_input:
            try:
                discount_percentage = float(discount_input)
                
                if discount_percentage < 0 or discount_percentage > 100:
                    messagebox.showerror("Error", "Please enter a valid discount percentage (0-100)", parent=self.root)
                    return
                
                # Calculate the discount amount
                self.discount = (discount_percentage / 100) * self.bill_amnt
            except ValueError:
                messagebox.showerror("Error", "Invalid discount value", parent=self.root)
                return
        else:
            self.discount = 0  # If no discount is entered, set it to 0
        
        # Calculate the net pay after applying the discount
        self.net_pay = self.bill_amnt - self.discount
        
        # Update the labels with the new values
        self.lbl_amnt.config(text=f"Bill Amt\n[{str(self.bill_amnt)}]")


                    # Show discount percentage and amount
                    # Show discount percentage and amount
                    # Show discount percentage and amount
                    # Show discount percentage and amount
                    #comment htate he screen pr discout show hoga


        # self.lbl_discount.config(text=f"Discount ({discount_percentage}%)\n[{str(self.discount)}]")  # Show discount percentage and amount
        self.lbl_net_pay.config(text=f"Net Pay\n[{str(self.net_pay)}]")
        self.cartTitle.config(text=f"Cart \t Total product: [{str(len(self.cart_list))}]")





    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)



    #=============%%%%%%%%%%%%%%%%%%%%%^^^^^^^^+++++++============
    def load_payments(self):
        """ 🚀 Load Payment Data """
        try:
            con = sqlite3.connect('ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM payments")
            rows = cur.fetchall()
            self.PaymentTable.delete(*self.PaymentTable.get_children())  # Clear previous data
            for row in rows:
                self.PaymentTable.insert('', END, values=row)  # Insert updated rows into the table
            con.close()
        except Exception as ex:
            messagebox.showerror("Database Error", f"Error due to: {str(ex)}", parent=self.root)








    #==================%%%%%%%%%%%%%%%%%^^^^^^^^^^^^^^++++=======






    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", "Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please add products to the cart!", parent=self.root)
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()

            # Save the bill to a file
            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been generated and saved", parent=self.root)
            self.chk_print = 1

            # Ask if the full amount is paid
            paid = messagebox.askquestion("Payment Status", "Is the full amount paid?")

            # If full amount is paid
            if paid == 'yes':
                self.var_payment_status.set("Paid")
                self.var_remaining_balance.set(0)  # Set balance to zero if full payment is made
            else:
                self.var_payment_status.set("Unpaid")
                remaining_balance = simpledialog.askfloat("Remaining Balance", "Enter the remaining balance:")
                if remaining_balance is None or remaining_balance < 0:
                    messagebox.showerror("Error", "Invalid remaining balance amount!", parent=self.root)
                    return
                self.var_remaining_balance.set(remaining_balance)


            # Save payment info in the database
            self.save_payment_info()
            
            self.chk_print = 1
            self.load_payments()














    def save_payment_info(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        # Insert payment information into the payments table
        cur.execute('''
            INSERT INTO payments (bill_id, amount_paid, payment_date, remaining_balance, payment_type, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.invoice,  # Bill ID
            self.bill_amnt,  # Amount paid
            time.strftime("%d-%m-%Y"),  # Payment date
            self.var_remaining_balance.get(),  # Remaining balance
            self.var_payment_status.get(),  # Paid/Unpaid status
            time.strftime("%d-%m-%Y")  # Due date (You can change this if you want a specific due date)
        ))

        con.commit()
        con.close()
        messagebox.showinfo("Payment Info", "Payment information has been saved.", parent=self.root)


    def update_payment(self):
        selected_item = self.PaymentTable.focus()  # Get the selected row
        if not selected_item:
            messagebox.showerror("Error", "Please select a payment record to update.", parent=self.root)
            return

        payment_data = self.PaymentTable.item(selected_item, 'values')
        if not payment_data:
            messagebox.showerror("Error", "Invalid selection.", parent=self.root)
            return

        payment_id = payment_data[0]  # Get payment_id from the selected row

        con = sqlite3.connect('ims.db')
        cur = con.cursor()

        try:
            # Update payment status to 'Paid' and remaining balance to 0
            cur.execute("UPDATE payments SET remaining_balance = 0, payment_type = 'Paid' WHERE payment_id = ?", (payment_id,))
            con.commit()
            con.close()

            messagebox.showinfo("Success", "Payment status updated to 'Paid' and remaining balance set to 0.", parent=self.root)

            self.load_payments()  # Refresh table with updated data
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating payment: {str(ex)}", parent=self.root)




        # Function to delete selected payment
    def delete_payment(self):
        """ 🗑️ Deletes a selected payment from the database & table """
        selected_item = self.PaymentTable.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete.", parent=self.root)
            return

        payment_data = self.PaymentTable.item(selected_item, "values")

        if not payment_data:
            messagebox.showerror("Error", "Invalid selection.", parent=self.root)
            return

        payment_id = payment_data[0]  # Get payment_id from selected row

        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete Payment ID {payment_id}?")

        if confirm:
            try:
                con = sqlite3.connect("ims.db")  # Ensure correct database name
                cur = con.cursor()

                # Delete the record from the database
                cur.execute("DELETE FROM payments WHERE payment_id = ?", (payment_id,))
                con.commit()
                con.close()

                # Remove from GUI table
                self.PaymentTable.delete(selected_item)

                # Show success message
                messagebox.showinfo("Success", "Payment record deleted successfully.")

                # Refresh the payment table
                self.load_payments()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record: {str(e)}", parent=self.root)














    
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%y"))
        print(self.invoice)
        bill_top_temp = '''
\t\t\t\t PAGDI CAFE AND RESTAURANT
\tPhone No. 98765***** , Delhi-125001
{0}
 Customer Name : {1}
 Phone No. : {2}
 Bill No. : {3}\t\t\t\t\tDate: {4}
{0}
 Product Name\t\t\tQTY\tPrice
{0}
'''.format("="*69, self.var_cname.get(), self.var_contact.get(), self.invoice, time.strftime("%d-%m-%Y"))

        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
    
    def bill_bottom(self):
        bill_bottom_temp = f'''
    {str("="*69)}
    Bill Amount\t\t\t\tRs.{self.bill_amnt}
    Discount ({self.var_discount.get()}%)\t\t\t\tRs.{self.discount}
    Net Pay\t\t\t\tRs.{self.net_pay}
    
    {str("="*68)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)



    
    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                     status='Inactive'
                if int(row[3])!=int(row[4]):
                     status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                # =====update qty in product table====== 
                cur.execute('UPDATE product SET qty=?,status=? where pid=?',(
                     qty,
                     status,
                     pid
                ))
                con.commit()

            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex )}",parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instok.config(text=f"In Stock")
        self.var_stock.set('')
         
    def clear_all(self):
        # Clear the cart list and reset the cart table
        del self.cart_list[:]  # Reset the cart list
        self.CartTable.delete(*self.CartTable.get_children())  # Clear the cart table display
        
        # Clear customer details
        self.var_cname.set('')  # Clear customer name
        self.var_contact.set('')  # Clear customer contact
        
        # Clear the bill area text
        self.txt_bill_area.delete('1.0', END)
        
        # Reset the cart title
        self.cartTitle.config(text=f"Cart \t Total product: [0]")
        
        # Reset the Bill Amount and Net Pay labels
        self.lbl_amnt.config(text="Bill Amount\n[0]")  # Reset bill amount label
        self.lbl_net_pay.config(text="Net Pay\n[0]")  # Reset net pay label
        
        # Reset the discount field and label
        self.var_discount.set('')  # Clear the discount entry field
        self.lbl_discount.config(text="Enter Discount (%)")  # Reset the discount label
        
        # Optionally, reset other parts of your UI (if applicable)
        self.clear_cart()  # Assuming this clears any remaining cart-related data
        
        # Refresh UI components (like showing cart data again)
        self.show()  # Ensure the show function updates your product list
        self.show_cart()  # Refresh the cart display (optional)

         
    def update_date_time(self):
         time_=time.strftime("%I:%M:%S")
         date_=time.strftime("%d-%m-%Y")
         self.lbl_clock.config(text=f"welcome to inventary management system\t\t date: {str(date_)}\t\t Time: {str(time_)} ")
         self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
     if self.chk_print == 1:
        messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
        new_file = tempfile.mktemp('.txt')
        with open(new_file, 'w') as f:
            f.write(self.txt_bill_area.get('1.0', END))

        # macOS printing command
        try:
            subprocess.run(['lp', new_file], check=True)  # Sends the file to the default printer
            os.remove(new_file)  # Clean up by deleting the temporary file after printing
        except Exception as e:
            messagebox.showerror('Print Error', f"An error occurred while printing: {str(e)}", parent=self.root)
     else:
        messagebox.showerror('Print', "Please generate the bill before printing the receipt", parent=self.root)
if __name__=="__main__": 

    root=Tk()
    obj=BillClass(root)
    root.mainloop()
