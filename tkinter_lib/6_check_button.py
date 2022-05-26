import tkinter as tk


def select_all():
    for check in [over_18, mailing, conditions]:
        check.select()


def deselect_all():
    for check in [over_18, mailing, conditions]:
        check.deselect()


def switch_all():
    for check in [over_18, mailing, conditions]:
        check.toggle()


def show_info():
    print("Adult: ", over_18_value.get())
    print("Mailing: ", mailing_value.get())


root = tk.Tk()
root.geometry("400x400")
root.title("My first GUI app")

over_18_value = tk.StringVar()
over_18_value.set("No")
over_18 = tk.Checkbutton(root, text="I'm 18",
                         variable=over_18_value,
                         onvalue="Yes",
                         offvalue="No"
                         )
over_18.pack()

mailing_value = tk.IntVar()
mailing = tk.Checkbutton(root, text="I want to receive mailing",
                         indicatoron=False,
                         variable=mailing_value,
                         onvalue=1,
                         offvalue=0
                         )
mailing.pack()

conditions = tk.Checkbutton(root, text="I've read all the conditions")
conditions.pack()

tk.Button(root, text="Select all", command=select_all).pack()
tk.Button(root, text="Deselect all", command=deselect_all).pack()
tk.Button(root, text="Switch all", command=switch_all).pack()
tk.Button(root, text="Show INFO", command=show_info).pack()

root.mainloop()