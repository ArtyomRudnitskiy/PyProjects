import tkinter as tk

# grid = table

root = tk.Tk()
root.geometry("400x400")
root.title("My first GUI app")

# kolkhoz
# btn1 = tk.Button(root, text="Hello1")
# btn2 = tk.Button(root, text="Hello2")
# btn3 = tk.Button(root, text="Hello3")
# btn4 = tk.Button(root, text="Hello world!")
# btn5 = tk.Button(root, text="Hello5")
# btn6 = tk.Button(root, text="Hello6")
# btn7 = tk.Button(root, text="Hello7")
# btn8 = tk.Button(root, text="Hello8")
#
# btn1.grid(row=0, column=0)
# btn2.grid(row=0, column=1, stick="we")
# btn3.grid(row=1, column=0)
# btn4.grid(row=1, column=1)
# btn5.grid(row=2, column=0)
# btn6.grid(row=2, column=1, stick="we")
# btn7.grid(row=3, column=0, columnspan=2, stick="we")  # big horizontal button
# btn8.grid(row=0, column=2, rowspan=4, stick="ns")  # big vertical button

# i = rows, j = columns
for i in range(5):
    for j in range(3):
        tk.Button(root, text=f"Hello {i},{j}").grid(row=i, column=j, stick="we")

root.columnconfigure(1, minsize=100)
root.columnconfigure(0, minsize=150)

root.mainloop()
