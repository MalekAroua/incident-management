from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

def user_Enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)
def email_Enter(event):
    if emailEntry.get() == 'Email':
        emailEntry.delete(0, END)

def password_Enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)
        passwordEntry.config(show='*')

def confirm_password_enter(event):
    if confirm_password_entry.get() == 'Confirm Password':
        confirm_password_entry.delete(0, END)
        confirm_password_entry.config(show='')

def Lock():
    lockKey.config(file='lo.png')
    passwordEntry.config(show='*')
    keyButton.config(command=show)

def show():
    lockKey.config(file='un.png')
    passwordEntry.config(show='')
    keyButton.config(command=Lock)

def log_User():
    root.destroy()
    import main
def clear():
    usernameEntry.delete(0, END)
    emailEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirm_password_entry.delete(0, END)
    confirm_var.set(0)
def connect_Database():
    if emailEntry.get() == '' or usernameEntry.get() == '' or confirm_password_entry.get() == '':
        messagebox.showerror('Error', 'Every Field is Obligatory.')
    elif passwordEntry.get() != confirm_password_entry.get():
        messagebox.showerror('Error', 'Password incongruity')
    elif confirm_var.get() == 0:
        messagebox.showerror('Error', 'Please Check the Confirm Information')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='1230')
            my_cursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connection Problem, Please Try Again')
            return
        try:
            query = 'create database userdata'
            my_cursor.execute(query)
            query = 'use userdata'
            my_cursor.execute(query)
            query = '''
                CREATE TABLE  data (
                    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                    username VARCHAR(100),
                    email VARCHAR(50),
                    password VARCHAR(20)
                )
                '''
            my_cursor.execute(query)

        except:
            my_cursor.execute('use userdata')
        query = 'select * from data where username=%s'
        my_cursor.execute(query, (usernameEntry.get()))

        row = my_cursor.fetchone()
        if row != None:
            messagebox.showerror('Error','Username Already Exist')
        else:
            query = 'insert into data(username,email,password) values(%s,%s,%s)'
            my_cursor.execute(query, (usernameEntry.get(),emailEntry.get(),passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Registration is successful')
            clear()
            root.destroy()
            import main


root = Tk()
root.title('Create Account')
root.geometry('1400x1000+0+0')
bgL = Label(root)
bgL.pack()

img = PhotoImage(file='pic.png')
Label(root, image=img, bg='white').place(x=0, y=0)

heading = Label(root, text='Create Account', font=('Arial Baltic', 23), bg='dark slate gray', fg='white')
heading.place(x=1100, y=99)

label_username = Label(root, text='Username:', font=('Arial', 12))
label_username.place(x=1100, y=159)
usernameEntry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12')
usernameEntry.place(x=1100, y=189)
usernameEntry.insert(0, 'Username')

usernameEntry.bind('<FocusIn>', user_Enter)


email_label = Label(root, text='Email:', font=('Arial', 12))
email_label.place(x=1100, y=239)
emailEntry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12')
emailEntry.place(x=1100, y=269)
emailEntry.insert(0, 'Email')

emailEntry.bind('<FocusIn>', email_Enter)

password_label = Label(root, text='Password:', font=('Arial', 12))
password_label.place(x=1100, y=299)
passwordEntry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12', show='*')
passwordEntry.place(x=1100, y=329)
passwordEntry.insert(0, 'Password')

passwordEntry.bind('<FocusIn>', password_Enter)

confirm_password_label = Label(root, text='Confirm Password:', font=('Arial', 12))
confirm_password_label.place(x=1100, y=359)
confirm_password_entry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12', show='*')
confirm_password_entry.place(x=1100, y=389)
confirm_password_entry.insert(0, 'Confirm Password')

confirm_password_entry.bind('<FocusIn>', confirm_password_enter)

confirm_var = IntVar()
confirm_check = Checkbutton(root, text='I confirm that my information is accurate', font=('Constantia', 9),
                            variable=confirm_var)
confirm_check.place(x=1100, y=420)

lockKey = PhotoImage(file='lo.png', width=1090, height=1030)
keyButton = Button(root, image=lockKey, width=20, height=20, bd=0, bg='gray99', activebackground='white', cursor='hand2'
                   , command=Lock)
keyButton.place(x=1300, y=329)

signupButton = Button(root, text='Signup', font=('Open Sans', 16, 'bold'), fg='white', bg='grey9', cursor='hand2', bd=0,
                      width=19, activebackground='cyan2', command=connect_Database)
signupButton.place(x=1100, y=450)

logintButton = Button(root, text='Login', width=10, height=2, bd=0,
                      activebackground='cyan2', cursor='hand2', font=('Arial', 10), fg='gold2', command=log_User)
logintButton.place(x=1090, y=499)

root.mainloop()
