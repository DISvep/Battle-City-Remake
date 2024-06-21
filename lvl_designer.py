import tkinter as tk


class PaintByCells:
    def __init__(self, root, rows=12, columns=16, cell_size=50):
        self.root = root
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.colors = {"brown": "W", "blue": "B", "red": "E", "white": ".", "green": "P"}
        self.current_color = "brown"
        self.grid = [["." for _ in range(columns)] for _ in range(rows)]

        self.canvas = tk.Canvas(root, width=columns * cell_size, height=rows * cell_size)
        self.canvas.pack()

        self.create_grid()
        self.setup_bindings()

    def create_grid(self):
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.root.bind("<Key>", self.change_color)

    def paint(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.columns:
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.current_color)
            self.grid[row][col] = self.colors[self.current_color]

    def change_color(self, event):
        if event.char == "w":
            self.current_color = "brown"
        elif event.char == "b":
            self.current_color = "blue"
        elif event.char == "e":
            self.current_color = "red"
        elif event.char == "c":
            self.current_color = "white"
        elif event.char == "p":
            self.current_color = "green"

    def save_painting(self):
        with open("painting.txt", "w") as f:
            for row in self.grid:
                f.write("".join(row) + "\n")

    def load_painting(self):
        try:
            with open("painting.txt", "r") as f:
                for row_idx, line in enumerate(f):
                    for col_idx, char in enumerate(line.strip()):
                        self.grid[row_idx][col_idx] = char
                        color = [k for k, v in self.colors.items() if v == char][0]
                        x1 = col_idx * self.cell_size
                        y1 = row_idx * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
        except FileNotFoundError:
            print("No saved painting found.")


root = tk.Tk()
app = PaintByCells(root)
tk.Button(root, text="Save", command=app.save_painting).pack()
tk.Button(root, text="Load", command=app.load_painting).pack()
root.mainloop()
