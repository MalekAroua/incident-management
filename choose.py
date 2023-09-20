import tkinter as tk
from tkinter import ttk
import os

def open_center_energy():
    os.system("python incidentmanagment.py")

def open_clima():
    os.system("python center_clima.py")

root = tk.Tk()
root.title("Choose Option")

frame = ttk.Frame(root, padding=20)
frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

title_label = ttk.Label(frame, text="Select an Option", font=('bookman old style', 16))
title_label.grid(column=0, row=0, columnspan=2, pady=10)

style = ttk.Style()
style.configure("TButton", padding=10, font=("Helvetica", 14))

center_energy_button = ttk.Button(frame, text="Center Energy", command=open_center_energy)
center_energy_button.grid(column=0, row=1, pady=10)

clima_button = ttk.Button(frame, text="Center Climate Control", command=open_clima)
clima_button.grid(column=1, row=1, pady=10)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

root.mainloop()


