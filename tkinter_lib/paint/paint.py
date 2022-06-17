import tkinter as tk

canvas_width = 700
canvas_height = 700

brush_size = 3
brush_color = "black"


def paint(event):
    global brush_size
    global brush_color
    x1 = event.x - brush_size
    x2 = event.x + brush_size
    y1 = event.y - brush_size
    y2 = event.y + brush_size
    paint_area.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)


def change_brush_size(new_size):
    global brush_size
    brush_size = new_size


def change_brush_color(new_color):
    global brush_color
    brush_color = new_color


root = tk.Tk()
root.title("Python Paint")

paint_area = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
paint_area.bind("<B1-Motion>", paint)

paint_area.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky="wens")

root.mainloop()
