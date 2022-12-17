import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        # для наследования: передали все возможные аргументы родительского класса
        super().__init__(*args, **kwargs)

        # настроили окно
        self.title("Graph builder")
        self.geometry('900x600')
        self.minsize(900, 600)

        # построили граф по умолчанию
        self.G = nx.Graph()

        self.G.add_node(1)

        # создаём интерфейс

        # =========
        # LEFT PART
        # =========

        # визуализация графа
        self.fig = plt.figure()
        nx.draw(self.G, with_labels=True)
        canvas = FigureCanvasTkAgg(self.fig,
                                   master=self)
        canvas.draw()

        # закрепляем рисунок в окне
        canvas.get_tk_widget().place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.6)

        # ==========
        # RIGHT PART
        # ==========

        # ввод вершины
        tk.Label(self, text="Значение вершины:").place(relx=0.63, rely=0.01, relheight=0.05)

        self.value_var = tk.StringVar()
        self.value_var.set("2")
        ip_input = ttk.Entry(self, textvariable=self.value_var)
        ip_input.place(relx=0.79, rely=0.01, relwidth=0.2, relheight=0.05)

        btn_add_node = ttk.Button(self, text="Добавить вершину", command=self.add_node)
        btn_add_node.place(relx=0.63, rely=0.07, relwidth=0.36, relheight=0.08)

        btn_del_node = ttk.Button(self, text="Удалить вершину", command=self.delete_node)
        btn_del_node.place(relx=0.63, rely=0.16, relwidth=0.36, relheight=0.08)

        # ввод ребра
        tk.Label(self, text="Ребро между").place(relx=0.63, rely=0.3, relheight=0.05)

        self.edge1_var = tk.StringVar()
        self.edge1_var.set("1")
        edge1_input = ttk.Entry(self, textvariable=self.edge1_var)
        edge1_input.place(relx=0.79, rely=0.3, relwidth=0.05, relheight=0.05)

        tk.Label(self, text="и").place(relx=0.88, rely=0.3, relheight=0.05)

        self.edge2_var = tk.StringVar()
        self.edge2_var.set("2")
        edge2_input = ttk.Entry(self, textvariable=self.edge2_var)
        edge2_input.place(relx=0.94, rely=0.3, relwidth=0.05, relheight=0.05)

        btn_add_edge = ttk.Button(self, text="Добавить ребро", command=self.add_edge)
        btn_add_edge.place(relx=0.63, rely=0.36, relwidth=0.36, relheight=0.08)

        btn_del_edge = ttk.Button(self, text="Удалить ребро", command=self.delete_edge)
        btn_del_edge.place(relx=0.63, rely=0.45, relwidth=0.36, relheight=0.08)

        # обход в ширину
        tk.Label(self, text="Начать с вершины:").place(relx=0.63, rely=0.59, relheight=0.05)

        self.bfs_var = tk.StringVar()
        self.bfs_var.set("1")
        ip_input = ttk.Entry(self, textvariable=self.bfs_var)
        ip_input.place(relx=0.79, rely=0.59, relwidth=0.2, relheight=0.05)

        btn_bfs = ttk.Button(self, text="Поиск в ширину", command=self.bfs)
        btn_bfs.place(relx=0.63, rely=0.65, relwidth=0.36, relheight=0.08)

        self.reslt_var = tk.StringVar()
        bfs_input = ttk.Entry(self, textvariable=self.reslt_var)
        bfs_input.place(relx=0.63, rely=0.74, relwidth=0.36, relheight=0.05)

        # работа с файлами
        btn_export = ttk.Button(self, text="Экспортировать граф в файл", command=self.export_graph)
        btn_export.place(relx=0.63, rely=0.82, relwidth=0.36, relheight=0.08)

        btn_import = ttk.Button(self, text="Импортировать граф из файла", command=self.import_graph)
        btn_import.place(relx=0.63, rely=0.91, relwidth=0.36, relheight=0.08)

    def add_node(self):

        # считываем значение для вершины
        try:
            node_value = int(self.value_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Значение вершины должно быть числом")
            return

        # добавляем вершину
        self.G.add_node(node_value)

        # перерисовываем рисунок
        self.redraw_graph()

    def delete_node(self):
        # считываем значение для вершины
        try:
            node_value = int(self.value_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Значение вершины должно быть числом")
            return

        # проверка, существует ли вершина
        if node_value not in self.G.nodes():
            messagebox.showerror("Ошибка", "Вершины с таким значением нет в графе")
            return

        # удаляем вершину
        self.G.remove_node(node_value)

        # перерисовываем рисунок
        self.redraw_graph()

    def add_edge(self):
        # считываем значение для вершины
        try:
            node1 = int(self.edge1_var.get())
            node2 = int(self.edge2_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Значение вершин должно быть числом")
            return

        # добавляем ребро
        self.G.add_edge(node1, node2)

        # перерисовываем граф
        self.redraw_graph()

    def delete_edge(self):
        # считываем значение для вершины
        try:
            node1 = int(self.edge1_var.get())
            node2 = int(self.edge2_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Значение вершин должно быть числом")
            return

        # проверка, существует ли ребро
        if (node1, node2) not in self.G.edges():
            messagebox.showerror("Ошибка", "Такого ребра нет в графе")
            return

        # удаляем ребро
        self.G.remove_edge(node1, node2)

        # перерисовываем граф
        self.redraw_graph()

    def bfs(self):
        # сначала получим все грани в виде списка
        edges = list(self.G.edges())

        if edges:
            # затем построим список (словарь) смежности (вершина: вершины, которые с ней соединены)
            adj_list = {}

            # проходим по первому столбцу списка граней, добавляя его значения в качестве ключа,
            # а значения второго столбца в качестве value к ключу
            for i in range(len(edges)):
                if edges[i][0] not in adj_list.keys():
                    adj_list[edges[i][0]] = set()
                adj_list[edges[i][0]].add(edges[i][1])

            # проходим по второму столбцу списка граней, добавляя его значения в качестве ключа,
            # а значения первого столбца в качестве value к ключу
            for i in range(len(edges)):
                if edges[i][1] not in adj_list.keys():
                    adj_list[edges[i][1]] = set()
                adj_list[edges[i][1]].add(edges[i][0])

            # обход графа в ширину
            try:
                source = int(self.bfs_var.get())  # стартовая вершина
            except ValueError:
                messagebox.showerror("Ошибка", "Значение стартовой вершины должно быть целым числом")
                return

            if source not in adj_list.keys():
                messagebox.showerror("Ошибка", "Заданной вершины нет в графе")
                return

            visited = set()  # множество посещённых вершин
            queue = deque([source])  # очередь вершин для посещения
            visited.add(source)  # сразу добавляем стартовую вершину в посещённые

            bfs_log = [source]  # список посещённых вершин

            # посещаем вершины, пока очередь не станет пустой
            while queue:
                current_v = queue.popleft()  # достаём первый в очереди элемент
                for neighbour in adj_list[current_v]:  # посещаем каждого его соседа
                    if neighbour not in visited:  # если он ещё не был посещён
                        visited.add(neighbour)  # добавляем его в посещённые
                        queue.append(neighbour)  # добавляем его в очередь, чтобы потом посетить его соседей
                        bfs_log.append(neighbour)  # добавляем его в лог посещённых вершин

            # выводим в окно, в какой последовательности были посещены вершины (лог)
            self.reslt_var.set(', '.join(map(str, bfs_log)))
        else:
            messagebox.showerror("Ошибка", "В графе нет рёбер - обход невозможен")

    def export_graph(self):
        filepath = filedialog.askdirectory()

        if filepath != "":
            nx.write_edgelist(self.G, f'{filepath}\\graph.txt')
        else:
            messagebox.showerror("Ошибка", "Выберите папку, куда сохранить граф")

    def import_graph(self):
        filepath = filedialog.askopenfilename()

        try:
            if filepath != "":
                self.G = nx.read_edgelist(filepath, create_using=nx.Graph(), nodetype=int)
                self.redraw_graph()
            else:
                messagebox.showerror("Ошибка", "Выберите txt файл для импорта графа")
        except UnicodeDecodeError:
            messagebox.showerror("Ошибка", "Выберите txt файл для импорта графа")

    def redraw_graph(self):
        # перерисовываем рисунок
        self.fig.clear(True)
        nx.draw(self.G, with_labels=True)
        canvas = FigureCanvasTkAgg(self.fig,
                                   master=self)
        canvas.draw()

        # закрепляем рисунок в окне
        canvas.get_tk_widget().place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.6)


if __name__ == '__main__':
    app = App()
    app.mainloop()
