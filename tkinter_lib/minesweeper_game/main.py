import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror
from tkinter import ttk

colors = {
    1: "blue",
    2: "#008200",
    3: "#FF0000",
    4: "#000084",
    5: "#840000",
    6: "#008284",
    7: "#840084",
    8: "#000000"
}


class MineButton(tk.Button):

    def __init__(self, master, x, y, number=None, *args, **kwargs):
        super().__init__(master, width=3, font="Calibri 15 bold", *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.bomb_amount = 0
        self.is_open = False

    def __repr__(self):
        return f"Btn ({self.x},{self.y}) №{self.number} {self.is_mine}"


class MineSweeper:
    root = tk.Tk()
    ROWS = 6
    COLUMNS = 6
    MINES = 5
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.time_lbl = None
        self.mines_lbl = None
        self.buttons = []  # all the buttons of the playing field
        for i in range(MineSweeper.ROWS + 2):
            temp_list = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MineButton(MineSweeper.root, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_mouse_click)
                temp_list.append(btn)
            self.buttons.append(temp_list)

    def right_mouse_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return

        current_btn = event.widget

        # if there is no flag
        if current_btn["state"] == "normal":
            current_btn["state"] = "disabled"
            current_btn["text"] = "⚑"
            current_btn["disabledforeground"] = "red"

        # if there is flag
        elif current_btn["text"] == "⚑":
            current_btn["state"] = "normal"
            current_btn["text"] = ""

    def print_buttons(self):
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("B", end="")
                else:
                    print(btn.bomb_amount, end="")
            print()

    def click(self, clicked_button: MineButton):
        if MineSweeper.IS_GAME_OVER:
            return

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_bombs_around()
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", background="red", disabledforeground="black")
            MineSweeper.IS_GAME_OVER = True
            showinfo("Game over", "You lose!")
            for i in range(1, MineSweeper.ROWS + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn.config(text="*")

        else:
            if clicked_button.bomb_amount:
                color = colors.get(clicked_button.bomb_amount, 'black')
                clicked_button.config(text=clicked_button.bomb_amount, disabledforeground=color)
            else:
                self.search(clicked_button)

        clicked_button.config(state="disabled", relief=tk.SUNKEN)
        clicked_button.is_open = True

    def search(self, btn: MineButton):
        queue = [btn]
        while queue:
            current_btn = queue.pop()

            # if there are bombs around, open
            if current_btn.bomb_amount:
                color = colors.get(current_btn.bomb_amount, 'black')
                current_btn.config(text=current_btn.bomb_amount, disabledforeground=color)

            # if there aren't, search among neighbours
            else:
                x, y = current_btn.x, current_btn.y
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        neighbour = self.buttons[x + dx][y + dy]
                        if not neighbour.is_open and neighbour not in queue and 1 <= neighbour.x <= MineSweeper.ROWS \
                                and 1 <= neighbour.y <= MineSweeper.COLUMNS:
                            queue.append(neighbour)
            # ============================
            current_btn.is_open = True
            # ============================
            current_btn.config(state="disabled", relief=tk.SUNKEN)

    def add_widgets(self):

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        settings_bar = tk.Menu(self.root, tearoff=False)
        settings_bar.add_command(label="Play", command=self.reload)
        settings_bar.add_command(label="Settings", command=self.game_settings)
        settings_bar.add_command(label="Exit", command=self.root.destroy)

        menu_bar.add_cascade(label="Menu", menu=settings_bar)

        count = 1
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick="wens")  # add to field
                count += 1

        # configure buttons stretching
        for i in range(1, MineSweeper.ROWS + 1):
            tk.Grid.rowconfigure(self.root, i, weight=1)

        for j in range(1, MineSweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.root, j, weight=1)

        grid_mid = int(MineSweeper.COLUMNS/2)

        self.mines_lbl = tk.Label(self.root, text=f"Mines: {MineSweeper.MINES}")
        self.mines_lbl.grid(row=MineSweeper.ROWS + 2, column=1, columnspan=grid_mid)

        self.time_lbl = tk.Label(self.root, text=f"Time: 0")
        self.time_lbl.grid(row=MineSweeper.ROWS + 2, column=MineSweeper.COLUMNS-grid_mid+1, columnspan=grid_mid)

    def reload(self):
        [child.destroy() for child in self.root.winfo_children()]  # delete every widget
        self.__init__()
        self.add_widgets()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False

    def game_settings(self):
        win_settings = tk.Toplevel(self.root)
        win_settings.wm_title("Settings")

        tk.Label(win_settings, text="Number of rows: ").grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, str(MineSweeper.ROWS))
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(win_settings, text="Number of columns: ").grid(row=1, column=0)
        col_entry = tk.Entry(win_settings)
        col_entry.insert(0, str(MineSweeper.COLUMNS))
        col_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(win_settings, text="Number of mines: ").grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, str(MineSweeper.MINES))
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = ttk.Button(win_settings, text="Apply",
                             command=lambda: self.change_settings(row_entry, col_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, stick="we", padx=5, pady=5)

    def change_settings(self, row_entry, col_entry, mines_entry):
        try:
            MineSweeper.ROWS = int(row_entry.get())
            MineSweeper.COLUMNS = int(col_entry.get())
            MineSweeper.MINES = int(mines_entry.get())

            if MineSweeper.ROWS < 3:
                MineSweeper.ROWS = 3
            if MineSweeper.COLUMNS < 3:
                MineSweeper.COLUMNS = 3

            self.reload()
        except ValueError:
            showerror("Error", "Invalid input")

    def open_all_buttons(self):
        for i in range(MineSweeper.ROWS + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background="red", disabledforeground="black")
                elif btn.bomb_amount in colors:
                    color = colors.get(btn.bomb_amount, 'black')
                    btn.config(text=btn.bomb_amount, fg=color)

    # inheritance?
    def start(self):
        # self.open_all_buttons()
        self.add_widgets()

        MineSweeper.root.title("Minesweeper")
        MineSweeper.root.resizable(False, False)
        MineSweeper.root.mainloop()

    def insert_mines(self, number: int):
        mines_indexes = self.get_mines_indexes(number)
        # print(mines_indexes)
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in mines_indexes:
                    btn.is_mine = True

    def count_bombs_around(self):
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            neighbour = self.buttons[i + dx][j + dy]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.bomb_amount = count_bomb

    @staticmethod
    def get_mines_indexes(excluded_number):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROWS + 1))
        indexes.remove(excluded_number)
        shuffle(indexes)
        # print(indexes)
        return indexes[:MineSweeper.MINES]


if __name__ == '__main__':
    game = MineSweeper()
    game.start()

