import tkinter as tk

# create the main window and set title
root = tk.Tk()
root.title("My first GUI app")

# 2 versions to set geometry:
# root.geometry("400x400+100+200")
# or
h = w = 400
root.geometry(f"{h}x{w}+100+200")

# resizing settings
root.minsize(200, 200)
root.maxsize(600, 600)
root.resizable(True, True)

# change icon
icon = tk.PhotoImage(file="code.png")
root.iconphoto(False, icon)

# change background
root.config(bg="#f0933c")

root.mainloop()  # open mw

