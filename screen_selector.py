from grabber import Grabber
from processor import Processor
from pynput import keyboard
from win32api import GetSystemMetrics
import win32api
import win32gui
import win32con
import win32ui

global position
position = []

dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0, 0))
red = win32api.RGB(255, 0, 0)  # Red
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))


grab = Grabber()
process = Processor()


def draw_rect(pos: tuple[int, int, int, int], width, height, color):
    rect = win32gui.CreateRoundRectRgn(*monitor, 2, 2)
    win32gui.RedrawWindow(
        hwnd,
        monitor,
        rect,
        win32con.RDW_INVALIDATE | win32con.RDW_UPDATENOW | win32con.RDW_ERASE,
    )
    for x in range(width):
        win32gui.SetPixel(dc, pos[0] + x, pos[1], color)
        win32gui.SetPixel(dc, pos[0] + x, pos[1] + height, color)
    for y in range(height):
        win32gui.SetPixel(dc, pos[0], pos[1] + y, color)
        win32gui.SetPixel(dc, pos[0] + width, pos[1] + y, color)


def on_press(key):
    global position
    try:
        if key == keyboard.Key.ctrl_l:
            if len(position) > 1:
                width = abs(position[0][0] - position[1][0])
                height = abs(position[0][1] - position[1][1])
                coords = (*position[0], *position[1])
                draw_rect(coords, width, height, red)
                position.pop()

            if position:
                position.insert(1, win32gui.GetCursorPos())
            else:
                position.insert(0, win32gui.GetCursorPos())

    except AttributeError:
        pass


def on_release(key):
    global position
    try:
        if key == keyboard.Key.esc:
            return False
        if key == keyboard.Key.ctrl_l:
            if len(position) > 1:
                coords = [*position[0], *position[1]]
                grab.dimensions = (coords[0], coords[1], coords[2], coords[3])
                img = grab.capture_image()
                text = process.find_text(img)
                print(text)
                print("\n\n\n\n\n")
            position = []
    except AttributeError:
        pass


if __name__ == "__main__":

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:  # type: ignore
        listener.join()
