import tkinter as tk
from tkinter import ttk


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({ self.x}, { self.y})"


def show_info():
    print(f"Value of day: {combo_days.get()}\n"
          f"TYPE of day: {type(combo_days.get())}\n")

    print(f"Value of Point: {combo_points.get()}\n"
          f"TYPE of Point: {type(combo_points.get())}\n\n")  # IMPORTANT! CLASS IS 'STR'


def set_day():
    combo_days.set("Friday")


root = tk.Tk()
root.geometry("400x400")
root.title("My first GUI app")

week_days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

combo_days = ttk.Combobox(root, values=week_days, state="readonly")
combo_days.current(0)
combo_days.pack()

combo_points = ttk.Combobox(root, values=[Point(2, 3), Point(1, 3)])
combo_points.pack()

ttk.Button(root, text="Show INFO", command=show_info).pack()
ttk.Button(root, text="Set day", command=set_day).pack()

root.mainloop()