from tkinter import*
from tkinter import ttk,messagebox
import sqlite3
import os
import email_pass
import smtplib 
import time

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System | Developed By Himanshu Sharma & Jatin")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")
        self.root.state('zoomed') # Opens full screen automatically

        self.otp=''
        self.employee_id=StringVar()
        self.password=StringVar()

        #=========================left panel==================================
        left_frame = Frame(self.root, bg="#2b68e8")
        left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        
        lbl_welcome = Label(left_frame, text="Welcome to\nInventory Management", font=("Segoe UI", 32, "bold"), bg="#2b68e8", fg="white", justify=LEFT)
        lbl_welcome.place(x=80, rely=0.20)

        
        Frame(left_frame, bg="white").place(x=85, rely=0.36, width=80, height=4)

        
        desc_text = (
            "This system analyzes your inventory data,\n"
            "then creates the respective logs and files needed\n"
            "for your business operations.\n\n"
            "Secure, fast, and easy to use."
        )
        lbl_desc = Label(left_frame, text=desc_text, font=("Segoe UI", 16), bg="#2b68e8", fg="white", justify=LEFT)
        lbl_desc.place(x=80, rely=0.43)

       


        # ============================ 2. RIGHT PANEL=============================================
         
        
        right_frame = Frame(self.root, bg="white")
        right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

       
        lbl_login_title = Label(right_frame, text="Enter the details.", font=("Segoe UI", 26, "bold"), bg="white", fg="#4b4b4b")
        lbl_login_title.place(x=100, rely=0.25)

       
        lbl_user = Label(right_frame, text="Employee ID", font=("Segoe UI", 12, "bold"), bg="white", fg="#747d8c")
        lbl_user.place(x=100, rely=0.36)
        
        
        txt_employee_id = Entry(right_frame, textvariable=self.employee_id, font=("Segoe UI", 15), bg="#f4f5f7", bd=0)
        txt_employee_id.place(x=100, rely=0.40, width=450, height=45)

        
        lbl_pass = Label(right_frame, text="Password", font=("Segoe UI", 12, "bold"), bg="white", fg="#747d8c")
        lbl_pass.place(x=100, rely=0.49)
        
        txt_pass = Entry(right_frame, textvariable=self.password, show="*", font=("Segoe UI", 15), bg="#f4f5f7", bd=0)
        txt_pass.place(x=100, rely=0.53, width=450, height=45)

        
        btn_forget = Button(right_frame, text="Forgot Password?", command=self.forget_window, font=("Segoe UI", 11, "bold"), bg="white", fg="#2b68e8", bd=0, activebackground="white", activeforeground="#1a46a0", cursor="hand2")
        btn_forget.place(x=415, rely=0.61)

        
        btn_login = Button(right_frame, text="Login", command=self.login, font=("Segoe UI", 16, "bold"), bg="#2b68e8", fg="white", cursor="hand2", bd=0, activebackground="#1a46a0", activeforeground="white")
        btn_login.place(x=100, rely=0.70, width=450, height=50)


    
    
    # =========================================================================
    
    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fields are required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid USERNAME/PASSWORD",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashbord.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error',"Employee ID must be required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Employee ID,try again",parent=self.root)
                else:
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #call send_email_function()
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("RESET PASSWORD")
                        self.forget_win.config(bg="white")
                        self.forget_win.geometry('400x380+500+150')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text='Reset Password',font=('goudy old style',15,'bold'),bg="#2b68e8",fg="white").pack(side=TOP,fill=X)

                        # --- OTP Section ---
                        lbl_otp = Label(self.forget_win, text="Enter OTP Send on Registered Email", font=("times new roman", 13, "bold"), bg="white", fg="#2f3542").place(x=20, y=60)
                        txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15), bg="#f4f5f7", bd=0)
                        txt_reset.place(x=20, y=90, width=250, height=30)
                        
                        self.btn_reset = Button(self.forget_win, text="SUBMIT", command=self.validate_otp, font=("times new roman", 12, "bold"), bg="#2b68e8", fg="white", bd=0, cursor="hand2")
                        self.btn_reset.place(x=280, y=90, width=100, height=32)
                        
                        Frame(self.forget_win, bg="#2b68e8").place(x=20, y=120, width=250, height=2) # Blue Underline

                        # --- New Password Section ---
                        lbl_new_pass = Label(self.forget_win, text="New Password", font=("times new roman", 13, "bold"), bg="white", fg="#2f3542").place(x=20, y=150)
                        txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=("times new roman", 15), bg="#f4f5f7", bd=0)
                        txt_new_pass.place(x=20, y=180, width=250, height=30)
                        Frame(self.forget_win, bg="#2b68e8").place(x=20, y=210, width=250, height=2) # Blue Underline

                        # --- Confirm Password Section ---
                        lbl_c_pass = Label(self.forget_win, text="Confirm Password", font=("times new roman", 13, "bold"), bg="white", fg="#2f3542").place(x=20, y=240)
                        txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=("times new roman", 15), bg="#f4f5f7", bd=0)
                        txt_c_pass.place(x=20, y=270, width=250, height=30)
                        Frame(self.forget_win, bg="#2b68e8").place(x=20, y=300, width=250, height=2)

                        # --- Update Button ---
                        self.btn_update = Button(self.forget_win, text="Update", command=self.update_password, state=DISABLED, font=("times new roman", 15, "bold"), bg="#2b68e8", fg="white", bd=0, cursor="hand2")
                        self.btn_update.place(x=150, y=330, width=100, height=35)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def update_password(self):
        if self.var_new_pass.get() == "" or self.var_conf_pass.get() == "":
            messagebox.showerror("Error", "Password is required", parent=self.forget_win)
        
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "New Password & Confirm Password must be same", parent=self.forget_win)
        
        else:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?", (self.var_new_pass.get(), self.employee_id.get()))
                con.commit()
                con.close() 
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_win)
                self.forget_win.destroy()

            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.forget_win)

    def validate_otp(self):
        if self.var_otp.get() == "":
            messagebox.showerror("Error", "Please enter OTP", parent=self.forget_win)
            return 

        try:
            if str(self.otp) == str(self.var_otp.get()):
                self.btn_update.config(state=NORMAL)
                self.btn_reset.config(state=DISABLED)
                messagebox.showinfo("Success", "OTP Validated, please enter new password", parent=self.forget_win)
            else:
                messagebox.showerror("Error", "Invalid OTP, Try again", parent=self.forget_win)
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.forget_win)

    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))

        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team'

        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'

if __name__=="__main__":
    root=Tk()
    obj=Login_System(root)
    root.mainloop()