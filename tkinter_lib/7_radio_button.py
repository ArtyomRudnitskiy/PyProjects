import tkinter as tk


def select_level():
    level = lvl_var.get()
    lvl_text_var.set(f"You've chosen {level} level")

    print(levels[level])


root = tk.Tk()
root.geometry("400x400")
root.title("My first GUI app")

# first buttons part
race_var = tk.IntVar()

tk.Label(root, text="Choose a race").pack()
tk.Radiobutton(root, text="Human", variable=race_var, value=1).pack()
tk.Radiobutton(root, text="Elf", variable=race_var, value=2).pack()
tk.Radiobutton(root, text="Orc", variable=race_var, value=3).pack()

# second buttons part
levels = {
    1: "Easy",
    2: "Middle",
    3: "Hard",
}

lvl_var = tk.IntVar()
lvl_text_var = tk.StringVar()

tk.Label(root, text="Choose the difficulty level").pack()

for level in sorted(levels):
    tk.Radiobutton(root, text=levels[level], variable=lvl_var, value=level, command=select_level).pack()

tk.Label(root, textvariable=lvl_text_var).pack()

root.mainloop()
