import tkinter as tk
from tkinter import Frame, BOTH, X, N, LEFT, RIGHT
from abc import ABC, abstractmethod
import threading

import control
import test


class Observer(ABC):

    @abstractmethod
    def update(self, subject) -> None:

        pass



class Listener(Observer):

    def update(self, subject):
        print(subject._weight)
        App.set_label(app, subject._weight)


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
        thr1 = threading.Thread(target = test.test_observer)
        thr1.start()

    def set_label(self, data):
        print(f'Setting label to: {str(data[2])}')
        self.label_brutto.config(text = 'Brutto: ' + str(data[2]))



if __name__ == "__main__":
    app = App()
    lis = Listener()
    control.anons.attach(lis)
    app.mainloop()