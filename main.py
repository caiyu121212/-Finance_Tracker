import tkinter as tk
from gui.main_window import MainWindow
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    try:
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
    except Exception as e:
        print(f"程序启动失败：{e}")
        input("按回车键退出...")

if __name__ == '__main__':
    main()