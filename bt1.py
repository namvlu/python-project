import tkinter as tk
from math import sqrt, log

win = tk.Tk()
win.title("Giả lập máy tính đơn giản")

entry = tk.Entry(win, width=40, borderwidth=5)
entry.grid(row=0, column=0, columnspan=6)

def press(key):
    current = entry.get()
    if key == "=":
        try:
            kq = eval(current)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(kq))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Lỗi nhập liệu, vui lòng thử lại")
    elif key == "Clear":
        entry.delete(0, tk.END)
    elif key == "Sqrt":
        try:
            kq = sqrt(float(current))
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(kq))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Lỗi nhập liệu, vui lòng thử lạii")
    elif key == "Log":
        try:
            kq = log(float(current))
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(kq))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Lỗi nhập liệu, vui lòng thử lại")
    elif key == "^":
        entry.insert(tk.END, "**")
    else:
        entry.insert(tk.END, key)

def block_key(event):
    return "break"

buttons = [
'7', '8', '9', '+', 'Sqrt',
'4', '5', '6', '-', 'Log',
'1', '2', '3', '*', '^',
'Clear', '0', '=', '/', '.']

entry.bind("<Key>", block_key)

row_value = 1
col_value = 0
for button in buttons:
    tk.Button(win, text=button, width=10, height=3, command=lambda b=button: press(b)).grid(row=row_value, column=col_value)
    col_value += 1
    if col_value > 4:
        col_value = 0
        row_value += 1

win.mainloop()
