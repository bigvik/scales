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
        App.set_label(app, subject)


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

        self.frame3 = Frame(self.frame)
        self.frame3.pack(fill=X)

        self.label_state = tk.Label(self.frame1, text='Состояние: ---', width=100)
        self.label_state.pack(side=LEFT, padx=5, pady=5)

        self.button_add = tk.Button(self.frame1, text = 'Тестировать', command=self.get_testweight)
        self.button_add.pack(side=LEFT, padx=5, pady=5)

        self.button_run = tk.Button(self.frame1, text = 'Запустить', command=self.get_weight)
        self.button_run.pack(side=LEFT, padx=5, pady=5)

        cols = ('Date', 'Brutto', 'Netto', 'Tara', 'Dist')
        self.listBox = ttk.Treeview(self.frame2, columns=cols, show='headings')
        # set column headings
        for col in cols:
            self.listBox.heading(col, text=col)    
        self.listBox.grid(row=1, column=0, columnspan=2)

        self.button_save = tk.Button(self.frame1, text = 'Сохранить', command=self.save)
        self.button_save.pack(side=LEFT, padx=5, pady=5)

    def switch_button_state(self):
        if (self.button_add['state'] == tk.NORMAL): self.button_add['state'] = tk.DISABLED
        else: self.button_add['state'] = tk.NORMAL

    def get_testweight(self):
        self.switch_button_state()
        thr = threading.Thread(target = test.test_observer)
        thr.start()
        self.switch_button_state()

    def get_weight():
        thr = threading.Thread(target = control.open_serial)
        thr.start()

    def set_label(self, data):
        self.label_state.config(text = 'Состояние: ' + data._msg)
        self.listBox.insert("", "end", values=(data._weight))

    def save(self):
        import datetime
        date = datetime.datetime.now().strftime('%d.%m.%Y')
        control.anons.set_msg(f'Сохранение в measurements_{date}.xlsx')
        control.ds.to_xlsbydate(date)
        control.anons.set_msg(f'measurements_{date}.xlsx сохранен в папке xlsx')



if __name__ == "__main__":
    app = App()
    lis = Listener()
    control.anons.attach(lis)
    app.mainloop()