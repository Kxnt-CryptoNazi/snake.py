import tkinter as tk
import random

WIDTH = 600
HEIGHT = 600
DOT_SIZE = 20
DELAY = 100

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#111")
        self.canvas.pack()

        self.root.bind("<Key>", self.change_direction)

        self.show_start_screen()

    # ------------------ SCREENS ------------------

    def show_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 20,
                                text="SNAKE GAME",
                                fill="white",
                                font=("Arial", 30, "bold"))

        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 20,
                                text="Press SPACE to Start",
                                fill="gray",
                                font=("Arial", 16))

        self.root.bind("<space>", lambda e: self.start_game())

    def game_over_screen(self):
        self.canvas.create_text(WIDTH//2, HEIGHT//2,
                                text="GAME OVER",
                                fill="red",
                                font=("Arial", 28, "bold"))

        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 40,
                                text="Press R to Restart",
                                fill="white")

        self.root.bind("r", lambda e: self.start_game())

    # ------------------ GAME ------------------

    def start_game(self):
        self.direction = "Right"
        self.snake = [(100,100),(80,100),(60,100)]
        self.food = self.spawn_food()
        self.score = 0
        self.running = True

        self.move()

    def spawn_food(self):
        while True:
            x = random.randint(0, (WIDTH - DOT_SIZE)//DOT_SIZE) * DOT_SIZE
            y = random.randint(0, (HEIGHT - DOT_SIZE)//DOT_SIZE) * DOT_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, event):
        key = event.keysym
        opposite = {"Up":"Down","Down":"Up","Left":"Right","Right":"Left"}

        if key in opposite and key != opposite.get(self.direction):
            self.direction = key

    def move(self):
        if not self.running:
            return

        x, y = self.snake[0]

        if self.direction == "Up": y -= DOT_SIZE
        elif self.direction == "Down": y += DOT_SIZE
        elif self.direction == "Left": x -= DOT_SIZE
        elif self.direction == "Right": x += DOT_SIZE

        new_head = (x, y)

        # Collision
        if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in self.snake):
            self.running = False
            self.draw()
            self.game_over_screen()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        self.draw()
        self.root.after(DELAY, self.move)

    # ------------------ DRAWING ------------------

    def draw(self):
        self.canvas.delete("all")

        # --- Snake (smooth body) ---
        points = []
        for x, y in self.snake:
            points.extend([x + DOT_SIZE//2, y + DOT_SIZE//2])

        if len(points) >= 4:
            self.canvas.create_line(
                points,
                fill="#2ecc71",
                width=DOT_SIZE,
                smooth=True,
                splinesteps=20,
                capstyle=tk.ROUND
            )

        # Head
        hx, hy = self.snake[0]
        self.canvas.create_oval(hx, hy, hx+DOT_SIZE, hy+DOT_SIZE, fill="#27ae60")

        # Eyes
        self.canvas.create_oval(hx+5, hy+5, hx+9, hy+9, fill="white")
        self.canvas.create_oval(hx+11, hy+5, hx+15, hy+9, fill="white")

        # --- Apple (real shape) ---
        fx, fy = self.food

        self.canvas.create_polygon(
            fx+10, fy,
            fx+DOT_SIZE-10, fy,
            fx+DOT_SIZE, fy+10,
            fx+DOT_SIZE-5, fy+DOT_SIZE,
            fx+5, fy+DOT_SIZE,
            fx, fy+10,
            fill="red",
            smooth=True
        )

        # Stem
        self.canvas.create_line(
            fx + DOT_SIZE//2, fy,
            fx + DOT_SIZE//2, fy - 8,
            width=3,
            fill="brown"
        )

        # Leaf
        self.canvas.create_oval(
            fx + DOT_SIZE//2 + 2, fy - 10,
            fx + DOT_SIZE//2 + 10, fy - 2,
            fill="green"
        )

        # Score
        self.canvas.create_text(50, 20,
                                text=f"Score: {self.score}",
                                fill="white",
                                font=("Arial", 14))

# ------------------ RUN ------------------

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()