import tkinter as tk
import random


def say_hello():
    print("Hello!")


def add_label():
    lbl = tk.Label(root, text="New label")
    lbl.pack()


def counter_increment():
    global counter
    counter += 1
    btn4["text"] = f"Counter: {counter}"


def disable_buttons():
    if btn1["state"] == tk.DISABLED:
        for btn in buttons_list:
            btn["state"] = tk.NORMAL
    else:
        for btn in buttons_list:
            btn["state"] = tk.DISABLED


def bg_color():
    colors = ["red", "blue", "green", "white", "black"]
    root.config(bg=random.choice(colors))


root = tk.Tk()
root.geometry("400x400")
root.title("My first GUI app")
buttons_list = []

# first button "greater"
btn1 = tk.Button(root, text="PUSH ME",
                 command=say_hello
                 )
btn1.pack()
buttons_list.append(btn1)

# second button "label adder"
btn2 = tk.Button(root, text="DON'T PUSH ME",
                 command=add_label
                 )
btn2.pack()
buttons_list.append(btn2)

# third button "lambder"
btn3 = tk.Button(root, text="LAMBDA",
                 command=lambda: tk.Label(root, text="New lambda").pack()
                 )
btn3.pack()
buttons_list.append(btn3)

# forth button "incrementer"
counter = 0
btn4 = tk.Button(root, text=f"Counter: {counter}",
                 command=counter_increment,
                 bg="green",
                 activebackground="blue",
                 fg="white",
                 activeforeground="white",
                 state=tk.NORMAL,
                 )
btn4.pack()
buttons_list.append(btn4)

# fifth button "color changer"
btn5 = tk.Button(root, text="Change mw color",
                 command=bg_color)
btn5.pack()
buttons_list.append(btn5)

# sixth button "disabler"
btn6 = tk.Button(root, text="Disable all the buttons",
                 command=disable_buttons,
                 bg="red",
                 fg="white"
                 )
btn6.pack()

root.mainloop()
