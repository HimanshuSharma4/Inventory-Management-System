from tkinter import *
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.state('zoomed')

        # ==================== 1. HEADER ====================
        header_frame = Frame(self.root, bg="#010c48", height=70)
        header_frame.pack(side=TOP, fill=X)
        header_frame.pack_propagate(False) 

        self.icon_title = PhotoImage(file="images/logo1.png")
        Label(header_frame, text="Inventory Management System", image=self.icon_title, compound=LEFT, 
              font=("times new roman", 35, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).pack(side=LEFT, pady=10)

        Button(header_frame, text="Logout", command=self.logout, font=("times new roman", 15, "bold"), 
               bg="yellow", cursor="hand2", bd=2, width=10).pack(side=RIGHT, padx=20, pady=10)

        # ==================== 2. CLOCK ====================
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System | Date: DD-MM-YYYY | Time: HH:MM:SS", 
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.pack(side=TOP, fill=X)

        # ==================== 3. FOOTER ====================
        
        lbl_footer = Label(self.root, text="IMS-Inventory Management System | Developed By Himanshu Sharma & Jatin", 
                           font=("times new roman", 12), bg="#4d636d", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)

        # ==================== 4. MAIN BODY ====================
        
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(side=TOP, fill=BOTH, expand=True)

       # ---------------- LEFT MENU ----------------
        
        LeftMenu = Frame(main_frame, bd=2, relief=RIDGE, bg="white", width=250)
        LeftMenu.pack(side=LEFT, fill=Y)
        LeftMenu.pack_propagate(False)
        try:
            self.MenuLogo = Image.open("images/menu_im.png")
            self.MenuLogo = self.MenuLogo.resize((230, 160), Image.Resampling.LANCZOS)
            self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
            Label(LeftMenu, image=self.MenuLogo, bg="white").pack(side=TOP, fill=X)
        except Exception as e:
            pass 
        Label(LeftMenu, text="Menu", font=("times new roman", 20, "bold"), bg="#009688", fg="white").pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file="images/side.png") 
        btn_kwargs = {
            "image": self.icon_side, 
            "compound": LEFT, 
            "padx": 20, 
            "anchor": "w", 
            "font": ("times new roman", 16, "bold"), 
            "bg": "white", 
            "bd": 1, 
            "relief": SOLID,
            "cursor": "hand2"
        }
        
        Button(LeftMenu, text=" Employee", command=self.employee, **btn_kwargs).pack(side=TOP, fill=BOTH, expand=True)
        Button(LeftMenu, text=" Supplier", command=self.supplier, **btn_kwargs).pack(side=TOP, fill=BOTH, expand=True)
        Button(LeftMenu, text=" Category", command=self.category, **btn_kwargs).pack(side=TOP, fill=BOTH, expand=True)
        Button(LeftMenu, text=" Product", command=self.product, **btn_kwargs).pack(side=TOP, fill=BOTH, expand=True)
        Button(LeftMenu, text=" Sales", command=self.sales, **btn_kwargs).pack(side=TOP, fill=BOTH, expand=True)
        Button(LeftMenu, text=" Exit", command=self.root.destroy, **btn_kwargs).pack(side=TOP, fill=BOTH, expand=True)

        # ---------------- RIGHT CONTENT AREA (CARDS) ----------------
        
        RightContent = Frame(main_frame, bg="white")
        RightContent.pack(side=LEFT, fill=BOTH, expand=True)

        lbl_kwargs = {"bd": 5, "relief": RIDGE, "fg": "white", "font": ("goudy old style", 20, "bold")}
        
        self.lbl_employee = Label(RightContent, text="Total Employee\n[ 0 ]", bg="#33bbf9", **lbl_kwargs)
        self.lbl_employee.place(relx=0.05, rely=0.1, relwidth=0.26, relheight=0.25)

        self.lbl_supplier = Label(RightContent, text="Total Supplier\n[ 0 ]", bg="#ff5722", **lbl_kwargs)
        self.lbl_supplier.place(relx=0.37, rely=0.1, relwidth=0.26, relheight=0.25)

        self.lbl_category = Label(RightContent, text="Total Category\n[ 0 ]", bg="#009688", **lbl_kwargs)
        self.lbl_category.place(relx=0.69, rely=0.1, relwidth=0.26, relheight=0.25)

        self.lbl_product = Label(RightContent, text="Total Product\n[ 0 ]", bg="#607d8b", **lbl_kwargs)
        self.lbl_product.place(relx=0.21, rely=0.45, relwidth=0.26, relheight=0.25)

        self.lbl_sales = Label(RightContent, text="Total Sales\n[ 0 ]", bg="#ffc107", **lbl_kwargs)
        self.lbl_sales.place(relx=0.53, rely=0.45, relwidth=0.26, relheight=0.25)

        self.update_content()

    # ==================== METHODS ====================
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            self.lbl_product.config(text=f'Total Products\n[ {str(len(cur.fetchall()))} ]')

            cur.execute("select * from supplier")
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(cur.fetchall()))} ]')

            cur.execute("select * from category")
            self.lbl_category.config(text=f'Total Category\n[ {str(len(cur.fetchall()))} ]')

            cur.execute("select * from employee")
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(cur.fetchall()))} ]')
            
            if not os.path.exists('bill'):
                os.makedirs('bill')
            self.lbl_sales.config(text=f'Total Sales\n[ {str(len(os.listdir("bill")))} ]')

            time_ = time.strftime("%H:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System | Date: {str(date_)} | Time: {str(time_)}")
            self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            pass 
        finally:
            con.close()

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()