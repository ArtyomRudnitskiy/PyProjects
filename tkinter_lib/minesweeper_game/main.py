import tkinter as tk
from random import shuffle

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

    def __init__(self):
        self.buttons = []  # all the buttons of the playing field
        for i in range(MineSweeper.ROWS + 2):
            temp_list = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MineButton(MineSweeper.root, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                temp_list.append(btn)
                # btn.grid(row=i, column=j)  # add to field
            self.buttons.append(temp_list)

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
        if clicked_button.is_mine:
            clicked_button.config(text="*", background="red", disabledforeground="black")
            # ============================
            clicked_button.is_open = True
            # ============================
        else:
            if clicked_button.bomb_amount:
                color = colors.get(clicked_button.bomb_amount, 'black')
                clicked_button.config(text=clicked_button.bomb_amount, disabledforeground=color)
                # ============================
                clicked_button.is_open = True
                # ============================
            else:
                self.search(clicked_button)
        clicked_button.config(state="disabled", relief=tk.SUNKEN)

    def search(self, btn: MineButton):
        queue = [btn]
        while queue:
            current_btn = queue.pop()
            if current_btn.bomb_amount:
                color = colors.get(current_btn.bomb_amount, 'black')
                current_btn.config(text=current_btn.bomb_amount, disabledforeground=color)
            else:
                pass
            # ============================
            current_btn.is_open = True
            # ============================
            current_btn.config(state="disabled", relief=tk.SUNKEN)

            if not current_btn.bomb_amount:
                x, y = current_btn.x, current_btn.y
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if not abs(dx - dy) == 1:
                            continue

                        neighbour = self.buttons[x + dx][y + dy]
                        if not neighbour.is_open and neighbour not in queue and 1 <= neighbour.x <= MineSweeper.ROWS \
                                and 1 <= neighbour.y <= MineSweeper.COLUMNS:
                            queue.append(neighbour)

    def add_widgets(self):
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)  # add to field

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
        self.add_widgets()
        self.insert_mines()
        self.count_bombs_around()
        # self.open_all_buttons()
        self.print_buttons()

        MineSweeper.root.mainloop()

    def insert_mines(self):
        mines_indexes = self.get_mines_indexes()
        # print(mines_indexes)
        count = 1
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                if btn.number in mines_indexes:
                    btn.is_mine = True
                count += 1

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
    def get_mines_indexes():
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROWS + 1))
        shuffle(indexes)
        # print(indexes)
        return indexes[:MineSweeper.MINES]


if __name__ == '__main__':
    game = MineSweeper()
    game.start()
