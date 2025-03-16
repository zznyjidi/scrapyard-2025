import tkinter as tk
from tkinter import messagebox
import math
import random

def generate_star_points(cx, cy, outer_radius, inner_radius, num_points=5):
    """Generate points for a five-point star (closed polygon)."""
    points = []
    angle = math.radians(90)  # start at the top
    step = math.pi / num_points
    for i in range(num_points * 2):
        r = outer_radius if i % 2 == 0 else inner_radius
        x = cx + math.cos(angle) * r
        y = cy - math.sin(angle) * r  # canvas y increases downward
        points.append((x, y))
        angle += step
    points.append(points[0])  # close the star
    return points

def resample(points, num_samples):
    """Resample a polyline (list of points) to have a fixed number of points."""
    if len(points) < 2:
        return points
    # Compute cumulative distances along the points.
    dists = [0]
    for i in range(1, len(points)):
        d = math.dist(points[i-1], points[i])
        dists.append(dists[-1] + d)
    total_length = dists[-1]
    interval = total_length / (num_samples - 1)
    new_points = [points[0]]
    current_distance = interval
    i = 1
    while i < len(points) and len(new_points) < num_samples:
        while i < len(points) and dists[i] < current_distance:
            i += 1
        if i >= len(points):
            break
        p1 = points[i-1]
        p2 = points[i]
        d1 = dists[i-1]
        d2 = dists[i]
        t = 0 if d2 - d1 == 0 else (current_distance - d1) / (d2 - d1)
        x = p1[0] + t * (p2[0] - p1[0])
        y = p1[1] + t * (p2[1] - p1[1])
        new_points.append((x, y))
        current_distance += interval
    if len(new_points) < num_samples:
        new_points.append(points[-1])
    return new_points

def discrete_frechet(P, Q):
    """
    Compute the discrete Fréchet distance between two curves P and Q.
    A lower value indicates a closer match.
    """
    n = len(P)
    m = len(Q)
    ca = [[-1 for _ in range(m)] for _ in range(n)]
    def c(i, j):
        if ca[i][j] > -1:
            return ca[i][j]
        d = math.dist(P[i], Q[j])
        if i == 0 and j == 0:
            ca[i][j] = d
        elif i > 0 and j == 0:
            ca[i][j] = max(c(i-1, 0), d)
        elif i == 0 and j > 0:
            ca[i][j] = max(c(0, j-1), d)
        elif i > 0 and j > 0:
            ca[i][j] = max(min(c(i-1, j), c(i-1, j-1), c(i, j-1)), d)
        else:
            ca[i][j] = float('inf')
        return ca[i][j]
    return c(n-1, m-1)

class StarTracerApp:
    def __init__(self, master):
        self.master = master
        master.title("Star Tracer")
        self.canvas_width = 800
        self.canvas_height = 800

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Generate and draw the reference star shape (in blue)
        # Centered in the canvas with a larger size.
        self.star_points = generate_star_points(self.canvas_width/2, self.canvas_height/2, 300, 120)
        self.canvas.create_line(*self.flatten(self.star_points), fill="blue", width=2)

        # For storing the user's drawing.
        self.drawing_points = []
        self.current_line = None
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # Button to evaluate the trace.
        self.evaluate_button = tk.Button(master, text="Evaluate", command=self.evaluate_trace)
        self.evaluate_button.pack(pady=10)

    def flatten(self, points):
        """Flatten list of tuples to a list of coordinates."""
        return [coord for point in points for coord in point]

    def start_draw(self, event):
        self.drawing_points = [(event.x, event.y)]
        self.current_line = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="red", width=2)

    def draw(self, event):
        self.drawing_points.append((event.x, event.y))
        if self.current_line:
            coords = self.canvas.coords(self.current_line) + [event.x, event.y]
            self.canvas.coords(self.current_line, *coords)

    def end_draw(self, event):
        self.drawing_points.append((event.x, event.y))
        self.current_line = None

    def evaluate_trace(self):
        if len(self.drawing_points) < 2:
            messagebox.showinfo("Error", "Please trace the star first!")
            return
        # Resample both curves to a fixed number of points.
        num_samples = 100
        user_curve = resample(self.drawing_points, num_samples)
        star_curve = resample(self.star_points, num_samples)
        distance = discrete_frechet(user_curve, star_curve)
        
        # Set a higher threshold for a more forgiving score.
        threshold = 300  # Adjust this value to suit your desired difficulty.
        score = max(0, 100 - (distance / threshold * 100))
        score = min(100, score)
        
        messagebox.showinfo("Result", f"Fréchet distance: {distance:.2f}(Lower is better)")

if __name__ == "__main__":
    root = tk.Tk()
    app = StarTracerApp(root)
    root.mainloop()
