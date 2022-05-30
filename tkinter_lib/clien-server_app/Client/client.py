import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import socket
import pickle
from PIL import Image


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Client")
        self.geometry('1200x500')
        self.minsize(1200, 500)

        # =========
        # LEFT PART
        # =========

        # table of functions
        heads = ["ID", "Function", "Line width", "Line color", "Line type", "Grid", "From", "To"]
        self.func_table = ttk.Treeview(self, columns=heads, show="headings")

        for header in heads:
            self.func_table.heading(header, text=header, anchor="center")
            self.func_table.column(header, width=1, anchor="center")

        self.func_table.place(relx=0.01, relheight=0.9, relwidth=0.7)
        self.id = 1  # id for functions in the table
        self.functions = dict()  # contains all the functions (class) in the table

        # buttons under the table
        btn_get_graph = ttk.Button(self, text="Get graph", command=self.dialog_window)
        btn_get_graph.place(relx=0.06, rely=0.91, relwidth=0.1, relheight=0.08)

        btn_del_f = ttk.Button(self, text="Delete function", command=self.del_func_from_table)
        btn_del_f.place(relx=0.31, rely=0.91, relwidth=0.1, relheight=0.08)

        btn_add_f = ttk.Button(self, text="Add function", command=self.add_func_to_table)
        btn_add_f.place(relx=0.56, rely=0.91, relwidth=0.1, relheight=0.08)

        # ==========
        # RIGHT PART
        # ==========

        # IP input field
        tk.Label(self, text="Server IP").place(relx=0.72, relheight=0.05)

        self.ip_var = tk.StringVar()
        self.ip_var.set("127.0.0.1")  # LOCAL ip
        ip_input = ttk.Entry(self, textvariable=self.ip_var)
        ip_input.place(relx=0.72, rely=0.05, relwidth=0.27, relheight=0.05)

        # port input field
        tk.Label(self, text="Port").place(relx=0.72, rely=0.12, relheight=0.05)

        self.port_var = tk.StringVar()
        self.port_var.set("2000")  # LOCAL port
        port_input = ttk.Entry(self, textvariable=self.port_var)
        port_input.place(relx=0.72, rely=0.17, relwidth=0.27, relheight=0.05)

        # function input field
        tk.Label(self, text="Function").place(relx=0.72, rely=0.24, relheight=0.05)

        tk.Label(self, text="f(x) = ").place(relx=0.72, rely=0.29, relheight=0.05)
        self.func_var = tk.StringVar()
        func_input = ttk.Entry(self, textvariable=self.func_var)
        func_input.place(relx=0.75, rely=0.29, relwidth=0.24, relheight=0.05)

        # segment input field
        tk.Label(self, text="Construct a function on a segment").place(relx=0.72, rely=0.36, relheight=0.05)

        tk.Label(self, text="from").place(relx=0.72, rely=0.42, relwidth=0.03, relheight=0.05)
        self.from_var = tk.DoubleVar()
        from_input = ttk.Entry(self, textvariable=self.from_var)
        from_input.place(relx=0.75, rely=0.42, relwidth=0.1, relheight=0.05)

        tk.Label(self, text="to").place(relx=0.86, rely=0.42, relwidth=0.03, relheight=0.05)
        self.to_var = tk.DoubleVar()
        to_input = ttk.Entry(self, textvariable=self.to_var)
        to_input.place(relx=0.89, rely=0.42, relwidth=0.1, relheight=0.05)

        # graph grid choice
        self.grid_var = tk.BooleanVar()
        grid_checkbtn = ttk.Checkbutton(self, text='Graph grid', variable=self.grid_var)
        grid_checkbtn.place(relx=0.72, rely=0.49, relwidth=0.1, relheight=0.05)

        # line width scale
        tk.Label(self, text="Line width").place(relx=0.72, rely=0.56, relheight=0.05)

        lwidth_scale = ttk.Scale(self, from_=1, to=10, command=self.scale_label)
        lwidth_scale.place(relx=0.72, rely=0.62, relwidth=0.2, relheight=0.05)

        self.scale_var = tk.IntVar()  # this label shows number on the scale
        self.scale_var.set(1)  # default value
        ttk.Label(self, text=0, textvariable=self.scale_var).place(relx=0.93, rely=0.62, relwidth=0.07, relheight=0.05)

        # line type choice
        tk.Label(self, text="Line type").place(relx=0.72, rely=0.69, relheight=0.05)

        self.lrype_var = tk.StringVar()
        self.lrype_var.set("-")

        ttk.Radiobutton(self, text="-", variable=self.lrype_var, value="-").place(relx=0.72, rely=0.74)
        ttk.Radiobutton(self, text="-.-", variable=self.lrype_var, value="-.").place(relx=0.82, rely=0.74)
        ttk.Radiobutton(self, text="--", variable=self.lrype_var, value="--").place(relx=0.92, rely=0.74)

        # color button
        btn_color = ttk.Button(self, text="Color", command=self.choose_color)
        btn_color.place(relx=0.74, rely=0.91, relwidth=0.23, relheight=0.08)
        self.line_color = "black"  # default line color

    def get_graph(self):

        # connecting to server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.ip_var.get(), int(self.port_var.get())))
        except (ConnectionRefusedError, OSError):
            messagebox.showerror("Error", "Failed connection attempt")
            return

        # sending selected function
        func_index = self.func_table.selection()  # find selected function
        if len(func_index) == 0:
            messagebox.showerror("Error", "You need to select one function in the table")
            return
        elif len(func_index) > 1:
            messagebox.showerror("Error", "You can plot only one function graph")
            return
        else:
            function = self.functions[func_index[0]]  # get function to plot
            client.send(pickle.dumps(function))  # send function to plot

        # getting image from server
        file = open(f"client_plot{func_index[0]}.jpg", mode="wb")  # the plot will be here

        data = client.recv(2048)  # get plot from server and write it down
        while data:
            file.write(data)
            data = client.recv(2048)
        file.close()
        client.close()  # disconnect from server

        # show plot
        picture = Image.open(f"client_plot{func_index[0]}.jpg")
        picture.show()

    def dialog_window(self):
        answer = messagebox.askyesno(
            title="Question",
            message="Save graph?")
        if answer:
            self.get_graph()

    def del_func_from_table(self):
        indexes = self.func_table.selection()
        for index in indexes:
            self.functions.pop(index)
            self.func_table.delete(index)

    def scale_label(self, value):
        value = int(float(value))
        self.scale_var.set(value)

    def choose_color(self):
        color_code = tk.colorchooser.askcolor(title="Choose color:")
        self.line_color = color_code[1]

    def add_func_to_table(self):
        error_text = "Invalid input"
        try:
            if self.func_var.get() == "":
                error_text = "Field 'f(x)' is empty"
                raise ValueError

            if self.from_var.get() >= self.to_var.get():
                error_text = "Parameter 'from' should be less than 'to'"
                raise ValueError

            func_data = [self.id,
                         self.func_var.get(),
                         self.scale_var.get(),
                         self.line_color,
                         self.lrype_var.get(),
                         self.grid_var.get(),
                         self.from_var.get(),
                         self.to_var.get()
                         ]
            self.functions[self.func_table.insert(parent="", index=tk.END, values=func_data, iid=str(self.id))] = \
                Function(*func_data[1:])

            self.id += 1
        except ValueError:
            messagebox.showerror("Error",  error_text)


class Function:
    def __init__(self, expression, lwidth, lcolor, ltype, grid, from_, to):
        self.expression, self.lwidth, self.lcolor, self.ltype = expression, lwidth, lcolor, ltype
        self.grid, self.from_, self.to = grid, from_, to


if __name__ == '__main__':
    app = App()
    app.mainloop()
