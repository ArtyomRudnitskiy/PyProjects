import tkinter as tk
from tkinter import ttk, messagebox
import socket
import pickle
import matplotlib.pyplot as plt
import numpy
import numexpr as ne
import os
from PIL import Image
import re


class Function:
    def __init__(self, expression, lwidth, lcolor, ltype, grid, from_, to):
        self.expression, self.lwidth, self.lcolor, self.ltype = expression, lwidth, lcolor, ltype
        self.grid, self.from_, self.to = grid, from_, to


class ServerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.banned_ip = []

        self.title("Server")
        self.geometry('300x400')
        self.minsize(300, 400)

        # server control button
        self.start_btn = ttk.Button(self, text="Start the server", command=self.start_server)
        self.start_btn.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.1)

        self.server_ip_lbl = tk.Label(self, text=f"Server IP: 127.0.0.1")
        self.server_ip_lbl.place(relx=0.01, rely=0.14, relheight=0.05)

        # input address to ban
        tk.Label(self, text="IP for ban").place(relx=0.01, rely=0.26, relheight=0.05)

        self.ip_var = tk.StringVar()
        self.ip_input = ttk.Entry(self, textvariable=self.ip_var)
        self.ip_input.place(relx=0.01, rely=0.31, relwidth=0.98, relheight=0.05)

        # "add" button
        self.add_ip_btn = ttk.Button(self, text="Add", command=self.add_address)
        self.add_ip_btn.place(relx=0.01, rely=0.37, relwidth=0.98, relheight=0.08)

        # table of ip addresses
        heads = ["ID", "IP address"]
        self.ip_table = ttk.Treeview(self, columns=heads, show="headings")

        for header in heads:
            self.ip_table.heading(header, text=header, anchor="center")
            self.ip_table.column(header, width=1, anchor="center")

        self.ip_table.place(relx=0.01, rely=0.54, relheight=0.35, relwidth=0.98)
        self.id = 1  # id for addresses in the table

        # "del" button
        self.add_ip_btn = ttk.Button(self, text="Delete", command=self.del_address)
        self.add_ip_btn.place(relx=0.01, rely=0.9, relwidth=0.98, relheight=0.08)

    def start_server(self):
        # start server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get local ip and set it in label
        #server_ip = socket.gethostbyname(socket.gethostname())
        #self.server_ip_lbl.config(text=f"Server IP: {server_ip}")

        # start of receiving information
        server.bind(("127.0.0.1", 2000))
        server.listen(4)

        # HOW to fix it???
        while True:
            # connect to client
            client_socket, client_address = server.accept()
            # print(client_address)

            if client_address[0] in self.banned_ip:
                print("Banned ip")

                client_socket.recv(2048)
                # send ban image
                file = open("ip_banned.jpg", mode="rb")

                data = file.read(2048)
                while data:
                    client_socket.send(data)
                    data = file.read(2048)

                file.close()
                client_socket.close()  # disconnect
                continue

            # get function information from client
            data = client_socket.recv(2048)
            # ==========================
            # EOFError: Ran out of input
            # ==========================
            function = pickle.loads(data)  # convert information to a Function object

            # give information to build a graph
            self.plot_func(function)

            # open plot image after plot_func, read and send it
            file = open("plot.jpg", mode="rb")

            data = file.read(2048)
            while data:
                client_socket.send(data)
                data = file.read(2048)

            file.close()
            client_socket.close()  # disconnect

            # delete plot after sending
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "plot.jpg")
            os.remove(path)

    def plot_func(self, function: Function):
        # configure graph
        plt.title("Graph of the function y = " + function.expression)
        plt.xlabel("x")
        plt.ylabel("y")
        x = numpy.arange(float(function.from_), float(function.to), 0.1)

        # plot graph
        if function.grid:
            plt.grid()

        expression = self.exp(function.expression)

        try:
            plt.plot(x, ne.evaluate(expression),
                     color=function.lcolor,
                     linestyle=function.ltype,
                     linewidth=function.lwidth)

            plt.savefig("plot.jpg")
            fig, ax = plt.subplots()
            fig.clear(True)
        except Exception as ex:
            print("Error")
            picture = Image.open('func_error.jpg')
            picture.save('plot.jpg')

    @staticmethod
    def exp(f):
        """Fix functions for plot"""
        print(f)
        match = re.findall(r'\d[x]\d', str(f))  # заменить сначала хчислох
        for m in match:
            l = m.split("x")[0] + '*x*' + m.split("x")[1]
            f1 = f.replace(m, l)

        try:
            f = f1
        except Exception:
            pass

        match = re.findall(r'\d[x]', str(f))
        for m in match:
            l = m.split("x")[0] + '*x'
            f1 = f.replace(m, l)
        try:
            f = f1
        except Exception:
            pass

        match = re.findall(r'[x]\d', str(f))
        for m in match:
            l = "x*" + m.split("x")[1]
            f1 = f.replace(m, l)
        try:
            f = f1
        except Exception:
            pass

        f1 = f.replace('e^', 'exp')
        try:
            f = f1
        except Exception:
            pass

        f1 = f.replace('^', '**')
        try:
            f = f1
        except Exception:
            pass

        f1 = f.replace('ln', 'log')
        try:
            f = f1
        except Exception:
            pass

        return f

    def add_address(self):
        address = self.ip_var.get()
        # if ip is correct, add it to the table
        if len(address.split(".")) == 4:
            self.ip_var.set("")  # clear entry
            self.banned_ip.append(address)  # add to banned

            lst = [str(self.id), address]
            self.ip_table.insert(parent="", index=tk.END, values=lst, iid=str(self.id))
            self.id += 1
        else:
            messagebox.showerror("Error", "Wrong IP address!")

    def del_address(self):
        indexes = self.ip_table.selection()
        for index in indexes:
            ip = self.ip_table.item(index)["values"][1]  # get value of selected line
            self.banned_ip.remove(ip)  # delete from ban list
            self.ip_table.delete(index)


if __name__ == '__main__':
    app = ServerApp()
    app.mainloop()


