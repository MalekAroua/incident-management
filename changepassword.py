from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import pymysql

def user_Enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def newpassword_Enter(event):
    if newpasswordEntry.get() == 'Password':
        newpasswordEntry.delete(0, END)
        newpasswordEntry.config(show='*')

def confirm_password_enter(event):
    if confirm_password_entry.get() == 'Confirm Password':
        confirm_password_entry.delete(0, END)
        confirm_password_entry.config(show='')

def Lock():
    lockKey.config(file='lo.png')
    newpasswordEntry.config(show='*')
    keyButton.config(command=show)

def show():
    lockKey.config(file='un.png')
    newpasswordEntry.config(show='')
    keyButton.config(command=Lock)

def clear():
    usernameEntry.delete(0, END)
    newpasswordEntry.delete(0, END)
    confirm_password_entry.delete(0, END)

def connect_Database():
    if usernameEntry.get() == '' or newpasswordEntry.get() == '' or confirm_password_entry.get() == '':
        messagebox.showerror('Error', 'Every Field is Obligatory.')
    elif newpasswordEntry.get() != confirm_password_entry.get():
        messagebox.showerror('Error', 'Password incongruity')
    else:
        con = pymysql.connect(host='localhost', user='root', password='1230', database='userdata')
        my_cursor = con.cursor()
        query_select = 'select * from data where username=%(username)s'
        my_cursor.execute(query_select, {'username': usernameEntry.get()})
        row = my_cursor.fetchone()
        if row is None:
            messagebox.showerror('Error', 'Incorrect Username')
        else:
            query_update = 'update data set password=%(new_password)s where username=%(username)s'
            my_cursor.execute(query_update, {'new_password': newpasswordEntry.get(), 'username': usernameEntry.get()})
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Password is reset, Please login with the new password')
def save():
    root.destroy()
    import main


root = Tk()
root.title('Change Password')
root.geometry('1400x1000+0+0')
bgL = Label(root)
bgL.pack()

img = PhotoImage(file='pic.png')
Label(root, image=img, bg='white').place(x=0, y=0)

heading = Label(root, text='Change Password', font=('Arial Baltic', 23), bg='dark slate gray', fg='white')
heading.place(x=1100, y=99)

label_username = Label(root, text='Username:', font=('Arial', 12))
label_username.place(x=1100, y=159)
usernameEntry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12')
usernameEntry.place(x=1100, y=189)
usernameEntry.insert(0, 'Username')

usernameEntry.bind('<FocusIn>', user_Enter)

newpassword_label = Label(root, text='New Password:', font=('Arial', 12))
newpassword_label.place(x=1100, y=239)
newpasswordEntry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12', show='*')
newpasswordEntry.place(x=1100, y=269)
newpasswordEntry.insert(0, 'New Password')

newpasswordEntry.bind('<FocusIn>', newpassword_Enter)

confirm_password_label = Label(root, text='Confirm Password:', font=('Arial', 12))
confirm_password_label.place(x=1100, y=299)
confirm_password_entry = Entry(root, width=25, font=('Ms Sans Serif', 11, 'bold'), bd=0, fg='Gray12', show='*')
confirm_password_entry.place(x=1100, y=329)
confirm_password_entry.insert(0, 'Confirm Password')

confirm_password_entry.bind('<FocusIn>', confirm_password_enter)


lockKey = PhotoImage(file='lo.png', width=1090, height=1030)
keyButton = Button(root, image=lockKey, width=20, height=20, bd=0, bg='gray99', activebackground='white', cursor='hand2'
                   , command=Lock)
keyButton.place(x=1300, y=268)

signupButton = Button(root, text='Save', font=('Open Sans', 16, 'bold'), fg='white', bg='grey9', cursor='hand2', bd=0,
                      width=19, activebackground='cyan2', command=lambda: [connect_Database(), save()])
signupButton.place(x=1100, y=390)



root.mainloop()