import os
import shutil
import win32file
import win32api
import time

def copy_usb_files(source_drive, destination_folder):
    """复制U盘中的所有文件到目标文件夹"""
    for root, dirs, files in os.walk(source_drive):
        for dir in dirs:
            source_dir_path = os.path.join(root, dir)
            destination_dir_path = os.path.join(destination_folder, os.path.relpath(source_dir_path, source_drive))
            if not os.path.exists(destination_dir_path):
                os.makedirs(destination_dir_path)  # 创建目标文件夹
                print(f"Created directory: {destination_dir_path}")

        for file in files:
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_folder, os.path.relpath(source_file_path, source_drive))
            if not os.path.exists(destination_file_path):
                try:
                    # 复制文件到目标文件夹
                    shutil.copy2(source_file_path, destination_file_path)
                    print(f"Copied file: {source_file_path}")
                except Exception as e:
                    print(f"Error copying file: {e}")

# 设置目标文件夹
destination_folder = "D:\\"  # 替换为目标文件夹路径

while True:
    # 获取所有逻辑驱动器
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]  # 分割字符串并移除最后一个空字符串

    for drive in drives:
        drive_type = win32file.GetDriveType(drive)
        # 仅处理可移动驱动器（U盘）
        if drive_type == win32file.DRIVE_REMOVABLE:
            print(f"Found removable drive: {drive}")
            copy_usb_files(drive, destination_folder)

    time.sleep(10)  # 每10秒检测一次
