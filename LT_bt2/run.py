import tkinter as tk
from data_connect import DatabaseApp

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()