from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import pymysql

def user_Enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)
def password_Enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)
        passwordEntry.config(show='*')
def Lock():
    lockKey.config(file='lo.png')
    passwordEntry.config(show='*')
    keyButton.config(command=show)

def show():
    lockKey.config(file='un.png')
    passwordEntry.config(show='')
    keyButton.config(command=Lock)

def creatAc():
    root.destroy()
    import creatacc

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Every Field is Obligatory')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='1230')
            my_cursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connection Problem, Please Try Again')
            return
        query = 'use userdata'
        my_cursor.execute(query)
        query = 'select *from data where username=%s and password=%s'
        my_cursor.execute(query,(usernameEntry.get(), passwordEntry.get()))
        row = my_cursor.fetchone()

        if row == None:
            messagebox.showerror('Error', 'Invalid Username or Password')
        else:
            messagebox.showinfo('Welcome', 'Authentication was successful')
            import choose

def forget():
    root.destroy()
    import changepassword


root = Tk()
root.title('Login')
root.geometry('1400x1000+0+0')
bgL = Label(root)
bgL.pack()

img = PhotoImage(file='pic.png')
Label(root, image=img, bg='white').place(x=0, y=0)

heading = Label(root, text='User Login', font=('Arial Baltic', 23), bg='dark slate gray', fg='white')
heading.place(x=1100, y=99)

usernameEntry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12')
usernameEntry.place(x=1100,y=179)
usernameEntry.insert(0, 'Username')

usernameEntry.bind('<FocusIn>', user_Enter)

Frame1 = Frame(root, width=200, height=2, bg='gray99')
Frame1.place(x=1101, y=201)

passwordEntry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12')
passwordEntry.place(x=1100, y=209)
passwordEntry.insert(0, 'Password')

passwordEntry.bind('<FocusIn>',password_Enter)

Frame2 = Frame(root, width=200, height=2, bg='gray99')
Frame2.place(x=1101, y=231)
lockKey = PhotoImage(file='lo.png', width=1090, height=1030)

keyButton = Button(root, image=lockKey, width=20, height=20, bd=0, bg='gray99', activebackground='white', cursor='hand2',
                        command=Lock)
keyButton.place(x=1300, y=209)

forgetButton = Button(root, text='Forget Password ?', width=18, height=2, bd=0, bg='gray99', activebackground='cyan2',
                        cursor='hand2', font=('Constantia', 9), fg='gold2',command=forget)
forgetButton.place(x=1220, y=240)

loginButton = Button(root, text='Login', font=('Open Sans', 16, 'bold'), fg='white', bg='grey9', cursor='hand2',
                     bd=0, width=19, activebackground='cyan2', command=login)
loginButton.place(x=1100, y=319)

haveAccountButton = Button(root, text='Do You Have an Account?', width=22, height=2, bd=0, bg='gray99',
                            activebackground='cyan2', cursor='hand2', font=('Constantia', 9), fg='gold2',
                           command=creatAc)
haveAccountButton.place(x=1085, y=369)

root.mainloop()