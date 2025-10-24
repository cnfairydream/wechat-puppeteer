import win32gui
import win32con
import win32process
import psutil

def enum_windows_callback(hwnd, hwnd_list):
    # 如果窗口不可见，也先收集信息
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    hwnd_list.append((hwnd, pid))

def show_app_from_tray(process_name):
    hwnd_list = []
    win32gui.EnumWindows(enum_windows_callback, hwnd_list)

    target_hwnd = None
    for hwnd, pid in hwnd_list:
        print(hwnd, pid)
        try:
            # 根据进程名匹配
            if psutil.Process(pid).name().lower() == process_name.lower():
                target_hwnd = hwnd
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if target_hwnd:
        # 先让窗口显示出来
        win32gui.ShowWindow(target_hwnd, win32con.SW_SHOW)  # 还原窗口
        win32gui.SetForegroundWindow(target_hwnd)  # 激活窗口
        print(f"已显示窗口: {target_hwnd}")
    else:
        print("未找到该应用窗口")

if __name__ == '__main__':
    # 例如 QQ 在系统里的进程名是 QQ.exe
    show_app_from_tray('WeChat.exe')