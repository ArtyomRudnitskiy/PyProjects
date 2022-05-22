import tkinter as tk


def get_info():
    name_data = name.get()
    password_data = password.get()

    if name_data and password_data:
        print(f"Name: {name_data}\nPassword: {password_data}")
        name.delete(0, tk.END)
        password.delete(0, tk.END)
    else:
        print("Wrong input")


def erase_info():
    name.delete(0)


root = tk.Tk()
root.geometry("400x400")
root.title("My first GUI app")

tk.Label(root, text="Name:"). grid(row=0, column=0, stick="w")
tk.Label(root, text="Password:"). grid(row=1, column=0, stick="w")

name = tk.Entry(root)
password = tk.Entry(root, show="*")
name.grid(row=0, column=1)
password.grid(row=1, column=1)

tk.Button(root, text="Enter", command=get_info).grid(row=2, column=0, stick="we")
tk.Button(root, text="Erase", command=erase_info).grid(row=3, column=0, stick="we")
tk.Button(root, text="Insert", command=lambda: name.insert(0, "hello")).grid(row=4, column=0, stick="we")

root.columnconfigure(1, minsize=100)
root.columnconfigure(0, minsize=150)

root.mainloop()