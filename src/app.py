import typing as t
import tkinter as tk
import threading

from . import ui
from . import Plugin


class App:

    def __init__(self, plugins: t.List[Plugin]) -> None:
        self.plugins = plugins
        diagnostic = threading.Thread(target=self.diagnostic, daemon=True)
        ui.runbtn.config(command=diagnostic.start)

    def diagnostic(self) -> None:
        ui.runbtn.config(state=tk.DISABLED)
        for plugin in self.plugins:
            ui.insert(f'[{plugin.name}]')
            for line in plugin.run():
                ui.insert(line)
            ui.insert('')
        ui.runbtn.config(state=tk.NORMAL)

    def run(self) -> None:
        ui.root.mainloop()
