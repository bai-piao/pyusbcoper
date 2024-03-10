import os
import shutil
import win32file
import win32api
import win32con
import win32gui
import time

def copy_to_usb(source_dir, usb_drive):
    try:
        # 获取所有的文件和目录列表
        files = os.listdir(source_dir)
        # 遍历文件和目录
        for file_name in files:
            # 构建源文件路径和目标文件路径
            source_path = os.path.join(source_dir, file_name)
            destination_path = os.path.join(usb_drive, file_name)
            # 如果是文件，则复制到目标位置
            if os.path.isfile(source_path):
                shutil.copy2(source_path, destination_path)
            # 如果是目录，则递归调用函数
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)
        print("复制完成！")
    except Exception as e:
        print("复制过程中出现错误:", e)

# 隐藏窗口
def hide_window():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

hide_window()  # 隐藏窗口

def monitor_usb():
    drive_bits = win32file.GetLogicalDrives()
    drives = []
    # 获取所有驱动器
    for d in range(1, 26):
        mask = 1 << d
        if drive_bits & mask:
            drives.append(chr(ord('A') + d - 1) + ':\\')

    # 监听USB插入事件
    hDir = win32file.CreateFile(
        r'\\.\\NotificationManager',
        0,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    while True:
        results = win32file.ReadDirectoryChangesW(
            hDir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_DEVICE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
        )
        for action, file in results:
            if action == 1:
                for drive in drives:
                    if drive == file[:3]:
                        print(f"检测到USB插入：{drive}")
                        return drive

# 源文件目录
source_directory = "C:\\path\\to\\source"
# 监听USB插入
while True:
    usb_drive_mount_point = monitor_usb()
    if usb_drive_mount_point:
        print("开始复制文件...")
        # 显示窗口
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        copy_to_usb(source_directory, usb_drive_mount_point)
        break
    time.sleep(10)  # 每10秒监听一次

# 隐藏窗口
hide_window()  # 隐藏窗口
