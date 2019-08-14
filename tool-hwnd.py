import win32gui
import win32con
from sys import argv
def get_windows():
    def sort_windows(windows):
        sorted_windows = []

        # Find the first entry
        for window in windows:
            if window["hwnd_above"] == 0:
                sorted_windows.append(window)
                break
        else:
            raise(IndexError("Could not find first entry"))

        # Follow the trail
        while True:
            for window in windows:
                if sorted_windows[-1]["hwnd"] == window["hwnd_above"]:
                    sorted_windows.append(window)
                    break
            else:
                break

        # Remove hwnd_above
        for window in windows:
            del(window["hwnd_above"])

        return sorted_windows

    def enum_handler(hwnd, results):
        window_placement = win32gui.GetWindowPlacement(hwnd)
        results.append({
            "hwnd":hwnd,
            "hwnd_above":win32gui.GetWindow(hwnd, win32con.GW_HWNDPREV), # Window handle to above window
            "Title":win32gui.GetWindowText(hwnd),
            "visible":win32gui.IsWindowVisible(hwnd) == 1,
            # "minimized":window_placement[1] == win32con.SW_SHOWMINIMIZED,
            # "maximized":window_placement[1] == win32con.SW_SHOWMAXIMIZED,
            # "rectangle":win32gui.GetWindowRect(hwnd) #(left, top, right, bottom)
        })

    enumerated_windows = []
    win32gui.EnumWindows(enum_handler, enumerated_windows)
    return sort_windows(enumerated_windows)

if __name__ == "__main__":
    windows = get_windows()
    
    for window in windows:
        if window["Title"] == "" :
            continue #nếu xuất hiện điều kiện thì sẽ không làm gì va tiếp tục vòng lặp
        print(window)

    # for window in windows:
    #     if window["Title"] == arg:
    #         print(window)
        
