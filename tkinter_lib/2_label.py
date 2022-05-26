import tkinter as tk

root = tk.Tk()
root.geometry("400x400")
root.title("My first GUI app")

# create label widget
label_1 = tk.Label(root, text='''Hello World!
I'm here now ya ya ya!''',
                   bg="blue",
                   fg="white",
                   font=('Times New Roman', 20, 'italic'),
                   padx=20,  # in pixels
                   pady=10,
                   width=20,  # in letters
                   height=5,
                   anchor='nw',
                   relief=tk.RAISED,
                   bd=10,
                   justify=tk.CENTER  # paragraph alignment
                   )
label_1.pack()

root.mainloop()
