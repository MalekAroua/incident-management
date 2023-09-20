import tkinter as tk
from tkinter import ttk
import ttkthemes
import pymysql

# Establish a connection to the MySQL database
db = pymysql.connect(host='localhost', user='root', password='1230', database='equipment_db')
cursor = db.cursor()

# Sample data for equipment
equipment_data = {
    "HUAWEI": {
        "Categories": ["Access Card", "Subscriber Card", "Battery", "Energy Workshop", "Electrogen Group"],
        "Items": {}
    },
    "SIEMENS": {
        "Categories": ["Access Card", "Subscriber Card", "Battery", "Energy Workshop", "Electrogen Group"],
        "Items": {}
    },
    "ALCATEL": {
        "Categories": ["Access Card", "Subscriber Card", "Battery", "Energy Workshop", "Electrogen Group"],
        "Items": {}
    }
}

current_equipment_category = None
current_category = None

def show_equipment_categories(equipment_name):
    global current_equipment_category
    current_equipment_category = equipment_name

    categories_label.config(text=f'{equipment_name} Equipment Categories')

    categories_list.delete(0, tk.END)

    for category in equipment_data[equipment_name]["Categories"]:
        categories_list.insert(tk.END, category)

def show_equipment_details(event):
    global current_category

    category_index = event.widget.curselection()
    if category_index:
        category_index = category_index[0]
        selected_category = equipment_data[current_equipment_category]["Categories"][category_index]

        current_category = selected_category

        designation_label.config(text=f"{current_category} Designation:")
        quantity_label.config(text=f"{current_category} Quantity:")
        add_button.config(text=f"Add {current_category} Equipment")

        designation_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)

def add_equipment():
    global current_equipment_category, current_category

    designation = designation_entry.get()
    quantity = quantity_entry.get()

    if current_equipment_category in equipment_data:
        if current_category not in equipment_data[current_equipment_category]["Items"]:
            equipment_data[current_equipment_category]["Items"][current_category] = []
        equipment_data[current_equipment_category]["Items"][current_category].append((designation, quantity))

        equipment_list.insert(tk.END, f"{current_category}: Designation: {designation}, Quantity: {quantity}")

        designation_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)

def delete_equipment():
    global current_equipment_category, current_category

    selected_item_index = equipment_list.curselection()
    if selected_item_index:
        selected_item_index = selected_item_index[0]
        equipment_list.delete(selected_item_index)

        deleted_equipment = equipment_data[current_equipment_category]["Items"][current_category].pop(selected_item_index)

def update_equipment():
    updated_designation = updated_designation_entry.get()
    updated_quantity = updated_quantity_entry.get()

    selected_item_index = equipment_list.curselection()
    if selected_item_index and updated_designation and updated_quantity:
        selected_item_index = selected_item_index[0]

        equipment_id = selected_item_index + 1  # Assuming equipment IDs start from 1

        # Update the equipment in the database
        query = "UPDATE equipment SET designation=%s, quantity=%s WHERE id=%s"
        cursor.execute(query, (updated_designation, updated_quantity, equipment_id))
        db.commit()

        equipment_list.delete(selected_item_index)
        equipment_list.insert(selected_item_index, f"{current_category}: Designation: {updated_designation}, Quantity: {updated_quantity}")

        updated_designation_entry.delete(0, tk.END)
        updated_quantity_entry.delete(0, tk.END)

# Create the equipment table in the database if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_name VARCHAR(255),
    category VARCHAR(255),
    designation VARCHAR(255),
    quantity INT
)
"""
cursor.execute(create_table_query)
db.commit()

root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('yaru')
root.geometry('1174x680+50+20')
root.resizable(0, 0)
root.title('Center Energy')

headingLabel = ttk.Frame(root, style='Heading.TFrame')
headingLabel.place(x=0, y=160, width=2000, height=50)

logim = tk.PhotoImage(file='ima.png')
logl = ttk.Label(root, image=logim)
logl.grid(row=0, column=0)

e = 'Equipments'
elable = ttk.Label(root, text=e, font=('bookman old style', 50), style='Title.TLabel')
elable.place(x=400, y=0)

equipment_buttons = [
    'HUAWEI', 'SIEMENS', 'ALCATEL'
]

for i, equipment in enumerate(equipment_buttons):
    button = ttk.Button(headingLabel, text=equipment, width=45,
                        command=lambda equip=equipment: show_equipment_categories(equip))
    button.grid(row=0, column=i + 1, pady=10)

exitB = ttk.Button(headingLabel, text='Exit', width=45)
exitB.grid(row=0, column=len(equipment_buttons) + 1, pady=10)

categories_label = ttk.Label(root, text="", font=('bookman old style', 10))
categories_label.place(x=400, y=200)

categories_list = tk.Listbox(root, font=('bookman old style', 12))
categories_list.place(x=400, y=230, width=200, height=150)

categories_list.bind('<<ListboxSelect>>', show_equipment_details)

designation_label = ttk.Label(root, text="", font=('bookman old style', 10))
designation_label.place(x=380, y=400)

designation_entry = ttk.Entry(root)
designation_entry.place(x=560, y=400)

quantity_label = ttk.Label(root, text="", font=('bookman old style', 10))
quantity_label.place(x=380, y=450)

quantity_entry = ttk.Entry(root)
quantity_entry.place(x=550, y=450)

add_button = ttk.Button(root, text="", style='Add.TButton',
                    command=add_equipment)
add_button.place(x=500, y=500)

delete_button = ttk.Button(root, text="Delete Equipment", style='Delete.TButton',
                       command=delete_equipment)
delete_button.place(x=650, y=500)

equipment_list = tk.Listbox(root, font=('bookman old style', 12))
equipment_list.place(x=800, y=200, width=300, height=300)

updated_designation_label = ttk.Label(root, text="", font=('bookman old style', 10))
updated_designation_label.place(x=800, y=520)

updated_designation_entry = ttk.Entry(root)
updated_designation_entry.place(x=950, y=520)

updated_quantity_label = ttk.Label(root, text="", font=('bookman old style', 10))
updated_quantity_label.place(x=800, y=570)

updated_quantity_entry = ttk.Entry(root)
updated_quantity_entry.place(x=950, y=570)

update_button = ttk.Button(root, text="Update Equipment", style='Update.TButton',
                        command=update_equipment)
update_button.place(x=850, y=620)

root.mainloop()

