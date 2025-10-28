import tkinter as tk
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from src.gui.main_window import MainWindow
from config import Config

def main():
    try:
        db_dir = os.path.dirname(Config.DATABASE_PATH)
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
    except Exception as e:
        print(f"程序启动失败：{e}")
        input("按回车键退出...")

if __name__ == '__main__':
    main()