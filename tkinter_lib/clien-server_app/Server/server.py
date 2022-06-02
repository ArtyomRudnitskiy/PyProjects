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

        self.start_btn = ttk.Button(self, text="Get address", command=self.get_address)
        self.start_btn.place(relx=0.01, rely=0.13, relwidth=0.98, relheight=0.1)

        # input server port
        tk.Label(self, text="Server port:").place(relx=0.01, rely=0.24, relheight=0.05)

        self.port_var = tk.StringVar()
        self.port_var.set("2000")
        self.port_input = ttk.Entry(self, textvariable=self.port_var)
        self.port_input.place(relx=0.23, rely=0.24, relwidth=0.76, relheight=0.05)

        self.serv_ip_var = "unknown"
        self.server_ip_lbl = tk.Label(self, text=f"Server IP: {self.serv_ip_var}")
        self.server_ip_lbl.place(relx=0.01, rely=0.3, relheight=0.05)

        # input address to ban
        tk.Label(self, text="IP for ban:").place(relx=0.01, rely=0.39, relheight=0.05)

        self.ip_var = tk.StringVar()
        self.ip_input = ttk.Entry(self, textvariable=self.ip_var)
        self.ip_input.place(relx=0.23, rely=0.39, relwidth=0.76, relheight=0.05)

        # "add" button
        self.add_ip_btn = ttk.Button(self, text="Add", command=self.add_address)
        self.add_ip_btn.place(relx=0.01, rely=0.45, relwidth=0.98, relheight=0.08)

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

    def get_address(self):
        if self.port_var.get() == "":
            messagebox.showerror("Error", "First, enter the port")
            return

        try:
            int(self.port_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid server port")
            return

        # get server ip from socket lib
        server_ip = socket.gethostbyname(socket.gethostname())
        self.serv_ip_var = server_ip
        self.server_ip_lbl.config(text=f"Server IP: {server_ip}")
        self.port_input.config(state="disabled")

    def start_server(self):
        if self.serv_ip_var == "unknown":
            messagebox.showerror("Error", "You didn't press 'Get address'")
            return

        # start server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get local ip and set it in label
        # server_ip = socket.gethostbyname(socket.gethostname())
        # self.server_ip_lbl.config(text=f"Server IP: {server_ip}")
        print("Server IP: " + self.serv_ip_var)
        print("Server port: " + self.port_var.get())

        # start of receiving information
        server.bind((self.serv_ip_var, int(self.port_var.get())))
        server.listen(4)

        # HOW to fix it???
        while True:
            # connect to client
            client_socket, client_address = server.accept()
            # print(client_address)

            if client_address[0] in self.banned_ip:
                # print("Banned ip")

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
            # print("Error")
            picture = Image.open('func_error.jpg')
            picture.save('plot.jpg')

    @staticmethod
    def exp(func):
        """Fix functions for plot"""
        match = re.findall(r'\d[x]\d', str(func))  # заменить сначала хчислох
        print(match)

        for m in match:
            l = m.split("x")[0] + '*x*' + m.split("x")[1]
            f1 = func.replace(m, l)

        try:
            func = f1
        except Exception:
            pass

        match = re.findall(r'\d[x]', str(func))
        for m in match:
            l = m.split("x")[0] + '*x'
            f1 = func.replace(m, l)
        try:
            func = f1
        except Exception:
            pass

        match = re.findall(r'[x]\d', str(func))
        for m in match:
            l = "x*" + m.split("x")[1]
            f1 = func.replace(m, l)
        try:
            func = f1
        except Exception:
            pass

        f1 = func.replace('e^', 'exp')
        try:
            func = f1
        except Exception:
            pass

        f1 = func.replace('^', '**')
        try:
            func = f1
        except Exception:
            pass

        f1 = func.replace('ln', 'log')
        try:
            func = f1
        except Exception:
            pass

        return func

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


