import win32gui
import win32api
import win32con
import ctypes
from ctypes import wintypes
import time
from pynput import keyboard

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class ScreenHighlighter:
    def __init__(self):
        self.highlighting = False
        self.lines = []
        self.last_position = None

        self.ctrl_pressed = False
        self.alt_pressed = False
        self.shift_pressed = False

        user32.SetProcessDPIAware()

        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.keyboard_listener.start()

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

    def get_cursor_pos(self):
        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def draw_line(self, hdc, x1, y1, x2, y2):
        gdi32.MoveToEx(hdc, x1, y1, None)
        gdi32.LineTo(hdc, x2, y2)

    def run(self):
        dc = user32.GetDC(None)
        pen = gdi32.CreatePen(win32con.PS_SOLID, 3, 0x0000FFFF)  # Yellow color
        old_pen = gdi32.SelectObject(dc, pen)

        try:
            while True:
                if self.highlighting:
                    x, y = self.get_cursor_pos()
                    if self.last_position:
                        self.draw_line(dc, self.last_position[0], self.last_position[1], x, y)
                        self.lines.append((time.time(), x, y))
                    self.last_position = (x, y)
                else:
                    self.last_position = None

                # Fade out old lines
                current_time = time.time()
                self.lines = [line for line in self.lines if current_time - line[0] <= 5]

                # Redraw screen to clear old lines
                if not self.highlighting:
                    user32.RedrawWindow(None, None, None,
                                        win32con.RDW_ERASE | win32con.RDW_INVALIDATE |
                                        win32con.RDW_ALLCHILDREN | win32con.RDW_UPDATENOW)

                time.sleep(0.01)  # Small delay to reduce CPU usage

        finally:
            gdi32.SelectObject(dc, old_pen)
            gdi32.DeleteObject(pen)
            user32.ReleaseDC(None, dc)


if __name__ == "__main__":
    highlighter = ScreenHighlighter()
    highlighter.run()