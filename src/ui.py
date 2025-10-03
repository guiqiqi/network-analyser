import tkinter as tk
from tkinter import scrolledtext

def insert(data: str) -> None:
    logtext.config(state=tk.NORMAL)
    logtext.insert(tk.END, data + '\n')
    logtext.see(tk.END)
    logtext.config(state=tk.DISABLED)


def lcopy():
    logs = logtext.get('1.0', tk.END).strip()
    if logs:
        root.clipboard_clear()
        root.clipboard_append(logs)
        root.update()


root = tk.Tk()
root.state('zoomed')
root.title('Network Diagnostic')

logtext = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=60, height=20, state=tk.DISABLED)
logtext.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

btnframe = tk.Frame(root)
btnframe.pack(pady=5)
runbtn = tk.Button(btnframe, text='Run Diagnostic', width=10)
runbtn.pack(side=tk.LEFT, padx=5)
cpbtn = tk.Button(btnframe, text='Copy Log', command=lcopy, width=10)
cpbtn.pack(side=tk.LEFT, padx=5)
