import tkinter as tk
from tkinter import Frame, BOTH, X, N, LEFT, RIGHT

class App(tk.Tk):
	
    def __init__(self) -> None:
        super().__init__()

        self.x = 1

        self.frame = Frame()
        self.frame.pack(fill=BOTH, expand=True)

        self.frame1 = Frame(self.frame)
        self.frame1.pack(fill=X)

        self.label_brutto = tk.Label(self.frame1, text='Brutto:', width=10)
        self.label_brutto.pack(side=LEFT, padx=5, pady=5)

        self.label_tara = tk.Label(self.frame1, text='Tara:', width=10)
        self.label_tara.pack(side=LEFT, padx=5, pady=5)

        self.label_netto = tk.Label(self.frame1, text='Netto:', width=10)
        self.label_netto.pack(side=LEFT, padx=5, pady=5)

        self.button_add = tk.Button(self.frame1, text = 'Измерить', command=self.get_weight)
        self.button_add.pack(side=LEFT, padx=5, pady=5)

    def get_weight(self):
        self.label_brutto.config(text = 'Brutto: ' + str(self.x))
        self.x += 1


if __name__ == "__main__":
    app = App()
    app.mainloop()