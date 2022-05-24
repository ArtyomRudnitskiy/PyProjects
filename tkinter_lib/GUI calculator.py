import tkinter as tk
import re
from tkinter import PhotoImage
from tkinter import messagebox


def make_digit_button(digit: int):
    return tk.Button(text=str(digit), font="Colibri 12 bold", command=lambda: add_digit(digit))


def make_math_button(operation: str):
    return tk.Button(text=operation, font="Colibri 12 bold", bg="#BEBFC1", command=lambda: add_operation(operation))


def make_equal_button(equal: str):
    return tk.Button(text=equal, font="Colibri 12 bold", bg="#BEBFC1", command=lambda: calculate())


def make_clear_button():
    return tk.Button(text="C", font="Colibri 12 bold", bg="#BEBFC1", command=lambda: clear())


def make_erase_button():
    return tk.Button(text="<", font="Colibri 12 bold", bg="#BEBFC1", command=lambda: erase())


def make_change_button():
    return tk.Button(text="+/-", font="Colibri 12 bold", command=lambda: change_sign())


def make_float_button():
    return tk.Button(text=",", font="Colibri 12 bold", command=lambda: make_float())


def make_sqrt_button():
    icon = PhotoImage(file="sqrt.png")
    return tk.Button(image=icon, text="sda", font="Colibri 12 bold", command=lambda: calc_sqrt())


def add_digit(digit):
    expr_line["state"] = tk.NORMAL
    value = expr_line.get()
    expr_line.delete(0, tk.END)

    if value == "0" or value == "Result is undefined":
        expr_line.insert(0, str(digit))
    elif value[-1] == "0" and len(value) == 1 or value[-1] == "0" and value[-2] in "+-*/":
        expr_line.insert(0, value[:-1] + str(digit))
    else:
        expr_line.insert(0, value + str(digit))
    expr_line["state"] = tk.DISABLED


def add_operation(operation: str):
    expr_line["state"] = tk.NORMAL
    value = expr_line.get()
    if value == "Result is undefined":
        operation = ""
    elif value[-1] in "+-*/":
        value = value[:-1]
    elif compare_lists(["+", "-", "*", "/"], value):  # if one of operations in value
        calculate()
        value = expr_line.get()

    expr_line.delete(0, tk.END)
    expr_line.insert(0, value + operation)
    expr_line["state"] = tk.DISABLED


# we need to add the operator to the end of calculated expression (if it isn't equal sign)
def calculate():
    expr_line["state"] = tk.NORMAL
    value = expr_line.get()
    if value[-1] in "+-*/":
        value = value + value[:-1]
    expr_line.delete(0, tk.END)

    try:
        expr_line.insert(0, eval(value))
    except ArithmeticError:
        expr_line.insert(0, "Result is undefined")
        # messagebox.showerror("Attention!", "Zero division error")
    expr_line["state"] = tk.DISABLED


def clear():
    expr_line["state"] = tk.NORMAL
    expr_line.delete(0, tk.END)
    expr_line.insert(0, "0")
    expr_line["state"] = tk.DISABLED


def erase():
    expr_line["state"] = tk.NORMAL
    value = expr_line.get()
    expr_line.delete(0, tk.END)
    if value == "0":
        pass
    else:
        value = value[:-1]
    if len(value) == 0:
        value = "0"
    expr_line.insert(0, value)
    expr_line["state"] = tk.DISABLED


def change_sign():
    expr_line["state"] = tk.NORMAL
    value = expr_line.get()
    expr_line.delete(0, tk.END)
    if value[0] == "0" or value == "Result is undefined":
        pass
    else:
        if value[0] == "-":
            value = value[1:]
        else:
            value = "-" + value
    expr_line.insert(0, value)
    expr_line["state"] = tk.DISABLED


def make_float():
    expr_line["state"] = tk.NORMAL
    value = expr_line.get()
    value_lst = re.split(r"[+\-*/]", value)
    expr_line.delete(0, tk.END)

    if "." not in value_lst[-1] and value != "Result is undefined":
        value = value + "."

    expr_line.insert(0, value)
    expr_line["state"] = tk.DISABLED


def calc_sqrt():
    pass


def compare_lists(lst1, lst2):
    for element in lst1:
        if element in lst2:
            return True
    return False


def press_key(event):
    if event.char.isdigit():
        add_digit(event.char)
    elif event.char in "+-*/":
        add_operation(event.char)
    elif event.char == "\r":
        calculate()
    elif event.char == "\x08":
        erase()


root = tk.Tk()
root.geometry("270x340")
root.title("Calculator")
root['bg'] = "#EFEFEF"

root.bind("<Key>", press_key)

expr_line = tk.Entry(root, justify=tk.RIGHT, font="Colibri 17 bold")
expr_line.insert(0, "0")
expr_line["state"] = tk.DISABLED
expr_line.grid(row=0, column=0, columnspan=4, sticky="we", padx=2, pady=2)

make_sqrt_button().grid(row=1, column=0, stick="wens", padx=2, pady=2)
make_clear_button().grid(row=1, column=1, stick="wens", padx=2, pady=2)
make_erase_button().grid(row=1, column=2, stick="wens", padx=2, pady=2)
make_math_button("/").grid(row=1, column=3, stick="wens", padx=2, pady=2)

make_digit_button(7).grid(row=2, column=0, stick="wens", padx=2, pady=2)
make_digit_button(8).grid(row=2, column=1, stick="wens", padx=2, pady=2)
make_digit_button(9).grid(row=2, column=2, stick="wens", padx=2, pady=2)
make_math_button("*").grid(row=2, column=3, stick="wens", padx=2, pady=2)

make_digit_button(4).grid(row=3, column=0, stick="wens", padx=2, pady=2)
make_digit_button(5).grid(row=3, column=1, stick="wens", padx=2, pady=2)
make_digit_button(6).grid(row=3, column=2, stick="wens", padx=2, pady=2)
make_math_button("-").grid(row=3, column=3, stick="wens", padx=2, pady=2)

make_digit_button(1).grid(row=4, column=0, stick="wens", padx=2, pady=2)
make_digit_button(2).grid(row=4, column=1, stick="wens", padx=2, pady=2)
make_digit_button(3).grid(row=4, column=2, stick="wens", padx=2, pady=2)
make_math_button("+").grid(row=4, column=3, stick="wens", padx=2, pady=2)

make_change_button().grid(row=5, column=0, stick="wens", padx=2, pady=2)
make_digit_button(0).grid(row=5, column=1, stick="wens", padx=2, pady=2)
make_float_button().grid(row=5, column=2, stick="wens", padx=2, pady=2)
make_equal_button("=").grid(row=5, column=3, stick="wens", padx=2, pady=2)

root.grid_columnconfigure(0, minsize=60)
root.grid_columnconfigure(1, minsize=60)
root.grid_columnconfigure(2, minsize=60)
root.grid_columnconfigure(3, minsize=60)

root.grid_rowconfigure(1, minsize=60)
root.grid_rowconfigure(2, minsize=60)
root.grid_rowconfigure(3, minsize=60)
root.grid_rowconfigure(4, minsize=60)
root.grid_rowconfigure(5, minsize=60)

root.mainloop()
