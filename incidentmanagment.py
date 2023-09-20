from tkinter import *
from tkinter import ttk
import ttkthemes
import time
from tkinter import messagebox,filedialog
import pymysql
from datetime import datetime
import pandas

mycursor = None
addB = None
deleteB = None
showB = None
exportB = None

def exit():
    res = messagebox.askyesno('Confirm','Do you want to exit ?')
    if res:
        root.destroy()
    else:
        pass
def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    index = listtable.get_children()
    nlist = []
    for ind in index:
        content = listtable.item(ind)
        dlist = content['values']
        nlist.append(dlist)

    table = pandas.DataFrame(nlist, columns=['Id', 'Incident Services', 'Type_of_incident', 'Add Date',
                                             'Add Time', 'Dateincident'])
    table.to_csv(url, index=False)  # Change 'ind' to 'index'
    messagebox.showinfo('Success', 'Data is saved successfully')

def show_list():
    try:
        # Fetch and display data from the incident table
        query = 'SELECT * FROM incident'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        listtable.delete(*listtable.get_children())
        for data in fetched_data:
            datalist = list(data)
            listtable.insert('', END, values=datalist)
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Error: {str(e)}', parent=root)


def generate_unique_id(input_id):
    query = "SELECT id FROM incident WHERE id = %s"
    mycursor.execute(query, (input_id,))
    result = mycursor.fetchone()
    if not result:
        return input_id
    else:
        messagebox.showerror('Error', 'ID already exists. Please use a different ID.')
        return None

def delete():
    index = listtable.focus()
    print(index)
    content = listtable.item(index)
    contentid = content['values'][0]
    query = 'delete from incident where id=%s'
    mycursor.execute(query, contentid)
    con.commit()
    messagebox.showinfo('Deleted',f'Id{contentid} is deleted successfully')
    query = 'select * from incident'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    listtable.delete(*listtable.get_children())
    for data in fetched_data:
        listtable.insert('', END, values=data)

def add():
    def adddata(currentdate=None):
        if idEntry.get() == '' or isEntry.get() == '' or tyiEntry.get() == '' or diEntry.get() == '':
            messagebox.showerror('Error', 'Every Field is Obligatory', parent=addw)
        else:
            entered_date = diEntry.get()  # Get the date string from the input field
            current_year = datetime.now().year  # Get the current year
            date = f"{entered_date} {current_year}"  # Add the current year to the date

            formatted_date = time.strftime('%d/%m/%Y', time.strptime(date, '%d %b %Y'))
            currenttime = time.strftime('%H:%M:%S')
            entered_id = idEntry.get()
            unique_id = generate_unique_id(entered_id)
            if unique_id is None:
                return
            query = ('INSERT INTO incident (id, IncidentServices, Typeofincident, date, time, Dateincident) VALUES '
                     '(%s, %s, %s, %s, %s, %s)')
            data = (unique_id, isEntry.get(), tyiEntry.get(), currentdate, currenttime, formatted_date)
            try:
                mycursor.execute(query, data)
                con.commit()
                result = messagebox.askyesno('Confirm', 'Added successfully. Do you want to clear the form?')
                if result:
                    idEntry.delete(0, END)
                    isEntry.delete(0, END)
                    tyiEntry.delete(0, END)
                    diEntry.delete(0, END)
            except pymysql.Error as e:
                messagebox.showerror('Error', f'Database Error: {str(e)}', parent=addw)

    addw = Toplevel()
    addw.resizable(False, False)

    idla = Label(addw, text='Id', font=('bookman old style', 12))
    idla.grid(row=0, column=0, padx=30, pady=15)
    idEntry = Entry(addw, font=('bookman old style', 12), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    isla = Label(addw, text='Incident Services', font=('bookman old style', 12))
    isla.grid(row=1, column=0, padx=30, pady=15)
    isEntry = Entry(addw, font=('bookman old style', 12), width=24)
    isEntry.grid(row=1, column=1, pady=15, padx=10)

    tyila = Label(addw, text='Type of incident ', font=('bookman old style', 12))
    tyila.grid(row=2, column=0, padx=30, pady=15)
    tyiEntry = Entry(addw, font=('bookman old style', 12), width=24)
    tyiEntry.grid(row=2, column=1, pady=15, padx=10)

    dila = Label(addw, text='Date incident', font=('bookman old style', 12))
    dila.grid(row=3, column=0, padx=30, pady=15)
    diEntry = Entry(addw, font=('bookman old style', 12), width=24)
    diEntry.grid(row=3, column=1, pady=15, padx=10)

    adde = ttk.Button(addw, text='Add Incident', command=lambda: adddata(diEntry.get()))
    adde.grid(row=4, columnspan=2, pady=15)

def connect():
    global mycursor, con, addB, deleteB, showB, exportB, listtable
    try:
        con = pymysql.connect(host='localhost', user='root', password='1230')
        mycursor = con.cursor()
        query = 'create database if not exists incident_management'
        mycursor.execute(query)
        query = 'use incident_management'
        mycursor.execute(query)
        query = ('create table if not exists incident (id int not null primary key auto_increment, '
                 'IncidentServices varchar(30), Typeofincident varchar(30), date varchar(50), time varchar(50),'
                 ' Dateincident varchar(50))')
        mycursor.execute(query)

        # Add this code to fetch and display data from the incident table
        query = 'SELECT * FROM incident'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        listtable.delete(*listtable.get_children())
        for data in fetched_data:
            datalist = list(data)
            listtable.insert('', END, values=datalist)

    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Error: {str(e)}', parent=root)
        return

    addB.config(state=DISABLED)
    deleteB.config(state=DISABLED)
    showB.config(state=DISABLED)
    exportB.config(state=DISABLED)
    root.update()
    root.after(100, show_success_message)

def show_success_message():
    messagebox.showinfo('Success', 'Database Connection is successful', parent=root)
    addB.config(state=NORMAL)
    deleteB.config(state=NORMAL)
    showB.config(state=NORMAL)
    exportB.config(state=NORMAL)

root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('yaru')
root.geometry('1280x880+50+50')
root.resizable(0, 0)
root.title('Incident Management')

headingLabel = Frame(root, bg='dark slate gray')
headingLabel.place(x=0, y=70, width=2000, height=50)

logim = PhotoImage(file='im.png')
logl = Label(root, image=logim)
logl.grid(row=0, column=0)

addB = ttk.Button(root, text='Add Incident', width=40, state=DISABLED, command=add)
addB.place(x=0, y=80)

deleteB = ttk.Button(root, text='Delete Incident', width=40, state=DISABLED, command=delete)
deleteB.place(x=290, y=80)

showB = ttk.Button(root, text='Show List', width=40, state=DISABLED, command=show_list)
showB.place(x=580, y=80)

exportB = ttk.Button(root, text='Export Data', width=40, state=DISABLED, command=export_data)
exportB.place(x=870, y=80)

exitB = ttk.Button(root, text='Exit', width=15, command=exit)
exitB.place(x=1160, y=80)

connectB = ttk.Button(root, text='Connect to database', command=connect)
connectB.place(x=1130, y=0)

middleframe = Frame(root)
middleframe.place(x=100, y=180, width=1150, height=250)

scrollx = Scrollbar(middleframe, orient=HORIZONTAL)
scrolly = Scrollbar(middleframe, orient=HORIZONTAL)

listtable = ttk.Treeview(middleframe, columns=('Id', 'Incident Services', 'Type_of_incident',
                                               'Add Date', 'Add Time',  'Dateincident'), xscrollcommand=scrollx.set,
                         yscrollcommand=scrolly.set)

scrollx.config(command=listtable.xview)
scrolly.config(command=listtable.yview)

scrollx.pack(side=BOTTOM, fill=X)
scrolly.pack(side=BOTTOM, fill=Y)

listtable.pack(fill=BOTH, expand=1)

listtable.heading('Id', text='Id')
listtable.config(show='headings')
listtable.heading('Incident Services', text='Incident Services')
listtable.heading('Type_of_incident', text='Type of incident')
listtable.heading('Add Date', text='Add Date')
listtable.heading('Add Time', text='Add Time')
listtable.heading('Dateincident', text='Date incident')

root.mainloop()

