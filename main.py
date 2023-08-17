import tkinter as tk
from tkinter import ttk
from tkinter import Frame, BOTH, X, N, LEFT, RIGHT
from abc import ABC, abstractmethod
import threading

import control
import test


class Observer(ABC):
    '''Абстрактный слушатель'''

    @abstractmethod
    def update(self, subject) -> None:

        pass



class Listener(Observer):
    '''Конкретный слушатель'''

    def update(self, subject):
        print(subject._weight)
        App.set_label(app, subject._weight)


class App(tk.Tk):
    '''
    Класс визуального интерфейса tkinter
    '''
	
    def __init__(self) -> None:
        super().__init__()

        self.x = 1

        self.frame = Frame()
        self.frame.pack(fill=BOTH, expand=True)

        self.frame1 = Frame(self.frame)
        self.frame1.pack(fill=X)

        self.frame2 = Frame(self.frame)
        self.frame2.pack(fill=X)

        self.label_brutto = tk.Label(self.frame1, text='Brutto:', width=10)
        self.label_brutto.pack(side=LEFT, padx=5, pady=5)

        self.label_tara = tk.Label(self.frame1, text='Tara:', width=10)
        self.label_tara.pack(side=LEFT, padx=5, pady=5)

        self.label_netto = tk.Label(self.frame1, text='Netto:', width=10)
        self.label_netto.pack(side=LEFT, padx=5, pady=5)

        self.button_add = tk.Button(self.frame1, text = 'Тестировать', command=self.get_weight)
        self.button_add.pack(side=LEFT, padx=5, pady=5)

        cols = ('Date', 'Brutto', 'Netto', 'Tara', 'Dist')
        self.listBox = ttk.Treeview(self.frame2, columns=cols, show='headings')
        # set column headings
        for col in cols:
            self.listBox.heading(col, text=col)    
        self.listBox.grid(row=1, column=0, columnspan=2)

    def switch_button_state(self):
        if (self.button_add['state'] == tk.NORMAL): self.button_add['state'] = tk.DISABLED
        else: self.button_add['state'] = tk.NORMAL

    def get_weight(self):
        self.switch_button_state()
        thr1 = threading.Thread(target = test.test_observer)
        thr1.start()

    def set_label(self, data):
        print(f'Setting label to: {str(data[2])}')
        self.label_brutto.config(text = 'Brutto: ' + str(data[1]))
        self.label_tara.config(text = 'Tara: ' + str(data[2]))
        self.label_netto.config(text = 'Netto: ' + str(data[3]))
        self.listBox.insert("", "end", values=(data))



if __name__ == "__main__":
    app = App()
    lis = Listener()
    control.anons.attach(lis)
    app.mainloop()