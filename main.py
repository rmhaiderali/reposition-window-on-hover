import os
import time
import win32api
import pygetwindow as gw
from rich.console import Console
from pynput import mouse, keyboard

console = Console()


def main():
    l, t, r, b = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0))).get("Work")

    mode = os.getenv("MODE", "1")
    title = os.getenv("TITLE", "Picture")
    interval = os.getenv("INTERVAL", "0.1")
    shadow = os.getenv("SHADOW", "0:0:0:0")

    win = None
    is_top = None
    is_left = None
    alt_pressed = False

    if mode not in ("1", "2", "3"):
        console.print("MODE must be 1, 2, or 3")
        exit(1)

    try:
        interval = float(interval)
    except:
        console.print("INTERVAL must be a integer or float")
        exit(2)

    if shadow.count(":") != 3:
        console.print("SHADOW must be in format of top:right:bottom:left")
        exit(3)

    shadow = shadow.split(":")
    try:
        shadow = {
            "t": int(shadow[0]),
            "r": int(shadow[1]),
            "b": int(shadow[2]),
            "l": int(shadow[3]),
        }
    except:
        console.print("Each part of SHADOW must be a integer")
        exit(4)

    def on_press(key):
        nonlocal alt_pressed
        if key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            alt_pressed = True

    def on_release(key):
        nonlocal alt_pressed
        if key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            alt_pressed = False

    keyboard.Listener(on_press=on_press, on_release=on_release).start()

    mouse_c = mouse.Controller()

    def is_in_top_left():
        x, y = mouse_c.position
        return l < x < l + win.width and t < y < t + win.height

    def is_in_bottom_right():
        x, y = mouse_c.position
        return r - win.width < x < r and b - win.height < y < b

    def is_in_top_right():
        x, y = mouse_c.position
        return r - win.width < x < r and t < y < t + win.height

    def is_in_bottom_left():
        x, y = mouse_c.position
        return l < x < l + win.width and b - win.height < y < b

    def to_top_left():
        nonlocal win
        nonlocal is_top
        nonlocal is_left
        x = l - shadow["l"]
        y = t - shadow["t"]
        win.moveTo(x, y)
        is_top = True
        is_left = True
        console.print("moved to top left")

    def to_bottom_right():
        nonlocal win
        nonlocal is_top
        nonlocal is_left
        x = r - win.width + shadow["r"]
        y = b - win.height + shadow["b"]
        win.moveTo(x, y)
        is_top = False
        is_left = False
        console.print("moved to bottom right")

    def to_top_right():
        nonlocal win
        nonlocal is_top
        nonlocal is_left
        x = r - win.width + shadow["r"]
        y = t - shadow["t"]
        win.moveTo(x, y)
        is_top = True
        is_left = False
        console.print("moved to top right")

    def to_bottom_left():
        nonlocal win
        nonlocal is_top
        nonlocal is_left
        x = l - shadow["l"]
        y = b - win.height + shadow["b"]
        win.moveTo(x, y)
        is_top = False
        is_left = True
        console.print("moved to bottom left")

    try:
        win = gw.getWindowsWithTitle(title)[0]
        if mode == "1":
            to_top_left()
        elif mode == "2":
            to_top_right()
        elif mode == "3":
            to_top_left()
    except:
        pass

    try:
        while True:
            time.sleep(interval)

            try:
                win = gw.getWindowsWithTitle(title)[0]
            except:
                continue

            if not alt_pressed and mouse_c.position is not None:

                if mode == "1":
                    # top:left → bottom:right ⟳

                    if is_top:
                        if is_in_top_left():
                            to_bottom_right()
                    else:
                        if is_in_bottom_right():
                            to_top_left()

                elif mode == "2":
                    # top:right → bottom:left ⟳

                    if is_top:
                        if is_in_top_right():
                            to_bottom_left()
                    else:
                        if is_in_bottom_left():
                            to_top_right()

                elif mode == "3":
                    # top:left → top:right → bottom:right → bottom:left ⟳

                    if is_top and is_left:
                        if is_in_top_left():
                            to_top_right()
                    elif is_top and not is_left:
                        if is_in_top_right():
                            to_bottom_right()
                    elif not is_top and is_left:
                        if is_in_bottom_left():
                            to_top_left()
                    else:
                        if is_in_bottom_right():
                            to_bottom_left()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
