import tkinter as tk
from pynput import keyboard, mouse
import time


class ScreenHighlighter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 1.0)  # Fully opaque
        self.root.attributes("-transparentcolor", "white")  # Make white transparent
        self.root.config(cursor="none")

        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.highlighting = False
        self.lines = []
        self.last_position = None

        self.ctrl_pressed = False
        self.alt_pressed = False
        self.shift_pressed = False

        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener = mouse.Listener(on_move=self.on_move)

        self.keyboard_listener.start()
        self.mouse_listener.start()

    def on_press(self, key):
        if key == keyboard.Key.ctrl_l:
            self.ctrl_pressed = True
        elif key == keyboard.Key.alt_l:
            self.alt_pressed = True
        elif key == keyboard.Key.shift:
            self.shift_pressed = True

        self.highlighting = self.ctrl_pressed and self.alt_pressed and self.shift_pressed

    def on_release(self, key):
        if key == keyboard.Key.ctrl_l:
            self.ctrl_pressed = False
        elif key == keyboard.Key.alt_l:
            self.alt_pressed = False
        elif key == keyboard.Key.shift:
            self.shift_pressed = False

        self.highlighting = self.ctrl_pressed and self.alt_pressed and self.shift_pressed
        if not self.highlighting:
            self.last_position = None

    def on_move(self, x, y):
        if self.highlighting:
            if self.last_position:
                line = self.canvas.create_line(self.last_position[0], self.last_position[1], x, y,
                                               fill="yellow", width=3, capstyle=tk.ROUND, smooth=True)
                self.lines.append((line, time.time()))
            self.last_position = (x, y)
        else:
            self.last_position = None

    def fade_lines(self):
        current_time = time.time()
        for line, timestamp in self.lines[:]:
            if current_time - timestamp > 5:
                self.canvas.delete(line)
                self.lines.remove((line, timestamp))

        self.root.after(100, self.fade_lines)

    def run(self):
        self.fade_lines()
        self.root.mainloop()


if __name__ == "__main__":
    highlighter = ScreenHighlighter()
    highlighter.run()