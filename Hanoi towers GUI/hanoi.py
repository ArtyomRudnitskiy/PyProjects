import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Canvas


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        # для наследования: передали все возможные аргументы родительского класса
        super().__init__(*args, **kwargs)

        # ПЕРВОНАЧАЛЬНАЯ НАСТРОЙКА

        # настроили окно
        self.title("Graph builder")
        self.geometry('900x600')
        self.minsize(900, 600)
        self.resizable(width=False, height=False)

        # создали список для хранения шагов
        self.steps = []
        self.number_steps = []

        # создали счётчик - индекс шага, который будет выделяться
        self.selected_index = 0

        # создали списки дисков на каждом стрежне
        self.pins = [[], [], []]

        # словарь соответствия цвета и ширины для каждого диска
        self.disk_prop = {1: ['#4C6ACD', 15],
                          2: ['#6EB8EF', 20],
                          3: ['#7EDA52', 25],
                          4: ['#F2CD1A', 30],
                          5: ['#FF7709', 35],
                          6: ['#E01C0E', 40]}

        # ИНТЕРФЕЙС

        # построили граф по умолчанию
        self.C = Canvas(self, cursor='pencil', bg='white')

        # нарисовали стержни
        self.C.create_line(100, 180, 100, 600, width=7)
        self.C.create_line(270, 180, 270, 600, width=7)
        self.C.create_line(440, 180, 440, 600, width=7)

        # self.C.create_rectangle(60, 540, 140, 600, fill="#E01C0E")
        # self.C.create_rectangle(65, 480, 135, 540, fill="#FF7709")
        # self.C.create_rectangle(70, 420, 130, 480, fill="#F2CD1A")

        # self.C.delete("all")

        self.C.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.6)

        # ==========
        # RIGHT PART
        # ==========

        # ввод количества дисков с выпадающим списком
        tk.Label(self, text="Количество дисков:").place(relx=0.63, rely=0.01, relheight=0.05)

        self.level_input = ttk.Combobox(self, values=(3, 4, 5, 6), state='readonly')
        self.level_input.bind("<<ComboboxSelected>>", self.draw_tower)

        self.level_input.place(relx=0.79, rely=0.01, relwidth=0.2, relheight=0.05)

        # кнопка для запуска алгоритма
        self.get_btn = ttk.Button(self, text="Получить список шагов", command=self.get_steps)
        self.get_btn.place(relx=0.63, rely=0.08, relwidth=0.36, relheight=0.08)

        # отключим кнопку "получить шаги"
        self.get_btn['state'] = tk.DISABLED

        # список шагов
        tk.Label(self, text="Список шагов:").place(relx=0.63, rely=0.16, relheight=0.05)

        listbox_frame = tk.Frame(self)
        step_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)

        self.steps_var = tk.StringVar()
        self.step_listbox = tk.Listbox(listbox_frame,
                                       width=150, height=40,
                                       yscrollcommand=step_scrollbar.set,
                                       listvariable=self.steps_var)

        # отключаем выделение в списке мышкой
        self.step_listbox.bindtags((self.step_listbox, self, "all"))

        step_scrollbar.config(command=self.step_listbox.yview)
        step_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_listbox.pack()

        listbox_frame.place(relx=0.63, rely=0.22, relwidth=0.36, relheight=0.48)

        # кнопки навигации по списку
        btn_bfs = ttk.Button(self, text="Далее", command=self.next)
        btn_bfs.place(relx=0.63, rely=0.71, relwidth=0.17, relheight=0.08)

        btn_bfs = ttk.Button(self, text="Назад", command=self.back)
        btn_bfs.place(relx=0.82, rely=0.71, relwidth=0.17, relheight=0.08)

        # работа с файлами
        btn_export = ttk.Button(self, text="Экспортировать список шагов", command=self.steps_export)
        btn_export.place(relx=0.63, rely=0.82, relwidth=0.36, relheight=0.08)

        btn_import = ttk.Button(self, text="Импортировать количество дисков", command=self.level_import)
        btn_import.place(relx=0.63, rely=0.91, relwidth=0.36, relheight=0.08)

    def draw_tower(self, event=None):
        """Рисует башню с level дисков"""
        # обновляем число дисков
        # значит, нужно заново сделать все стержни пустыми и почистить старый список шагов
        self.pins = [[], [], []]
        self.number_steps = []
        self.steps = []
        self.steps_var.set(self.steps)

        # и потом положить на первый стержень столько дисков, сколько было указано в level
        level = int(self.level_input.get())
        self.pins[0] = [i for i in range(1, level+1)][::-1]

        # потом нарисуем пирамидки
        self.draw_pyramids()

        # и включаем кнопку "получить список"
        self.get_btn['state'] = tk.NORMAL

    def draw_pyramids(self):
        self.C.delete('all')

        self.C.create_line(100, 180, 100, 600, width=7)
        self.C.create_line(270, 180, 270, 600, width=7)
        self.C.create_line(440, 180, 440, 600, width=7)

        floors = [540, 480, 420, 360, 300, 240]
        centers = [100, 270, 440]

        # диски на первом стержне
        for j, pin in enumerate(self.pins):
            for i, num in enumerate(pin):
                self.C.create_rectangle(centers[j]-self.disk_prop[num][1], floors[i],
                                        centers[j]+self.disk_prop[num][1], floors[i]+60,
                                        fill=self.disk_prop[num][0])

    def get_steps(self):
        # отключим кнопку "получить шаги"
        self.get_btn['state'] = tk.DISABLED

        # заполнили список шагов
        self.hanoi(int(self.level_input.get()), 1, 2)

        # вывод списка шагов
        self.steps_var.set(self.steps)

        # если до этого какой-то пункт списка был выделен, снимаем выделение
        self.step_listbox.select_clear(self.selected_index)

        # обнуляем счётчик индекса для выделения
        self.selected_index = 0
        self.step_listbox.select_set(0)

        from_, to_ = self.number_steps[self.selected_index]

        self.pins[to_-1].append(self.pins[from_-1].pop())

        # рисуем пирамидки
        self.draw_pyramids()

    def hanoi(self, n, i, k):
        if n == 1:
            self.steps.append(f'Переместите диск 1 со стержня {i} на стержень {k}')
            self.number_steps.append([i, k])
        else:
            tmp = 6 - i - k
            self.hanoi(n-1, i, tmp)
            self.steps.append(f'Переместите диск {n} со стержня {i} на стержень {k}')
            self.number_steps.append([i, k])
            self.hanoi(n-1, tmp, k)

    def next(self):
        if self.selected_index + 1 < self.step_listbox.size():
            self.step_listbox.select_clear(self.selected_index)
            self.selected_index += 1
            self.step_listbox.select_set(self.selected_index)

            from_, to_ = self.number_steps[self.selected_index]

            self.pins[to_ - 1].append(self.pins[from_ - 1].pop())

            # рисуем пирамидки
            self.draw_pyramids()

    def back(self):
        if self.selected_index - 1 >= 0:
            to_, from_ = self.number_steps[self.selected_index]

            self.pins[to_ - 1].append(self.pins[from_ - 1].pop())

            # рисуем пирамидки
            self.draw_pyramids()

            self.step_listbox.select_clear(self.selected_index)
            self.selected_index -= 1
            self.step_listbox.select_set(self.selected_index)

    def steps_export(self):
        path = filedialog.askdirectory()

        if path != "":
            with open(f'{path}/steps.txt', 'w', encoding="utf-8") as f:
                for item in self.steps:
                    f.write(f'{item}\n')

    def level_import(self):
        path = filedialog.askopenfilename()

        if path != "":
            with open(path) as f:
                data = f.read()

                if len(data.split()) == 1:
                    try:
                        data = int(data)
                    except ValueError:
                        messagebox.showerror("Ошибка", "Количество должно быть целым числом")
                        return

                    if data > 0:
                        if data > 6:
                            data = 6

                        self.level_input.set(data)
                        self.draw_tower()
                        self.get_steps()
                    else:
                        messagebox.showerror("Ошибка", "Количество должно быть положительным числом")
                else:
                    messagebox.showerror("Ошибка", "Данные в файле некорректные")
        else:
            messagebox.showerror("Ошибка", "Выберите txt файл для импорта количества дисков")


if __name__ == '__main__':
    app = App()
    app.mainloop()
