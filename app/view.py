import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import threading
import datetime
import logging
from abc import ABC, abstractmethod

import control


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Create handlers
s_handler = logging.StreamHandler()
f_handler = logging.FileHandler('log.log')
s_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
# Create formatters and add it to handlers
s_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_handler.setFormatter(s_format)
f_handler.setFormatter(f_format)
# Add handlers to the logger
logger.addHandler(s_handler)
logger.addHandler(f_handler)


class LabelLogging(logging.Handler):
    '''Класс для вывода логов в статусбар'''

    def __init__(self, lbl) -> None:
        logging.Handler.__init__(self)
        self.lbl = lbl

    def emit(self, record) -> None:
        msg = self.format(record)
        def set_log():
            self.lbl.config(text=msg)
        self.lbl.after(0, set_log)


class Listener(ABC):
    '''Абстрактный слушатель'''

    @abstractmethod
    def update(self, subject) -> None:

        pass


class ViewListener(Listener):
    '''Слушатель для визуального интерфейса'''

    def update(self, subject):
        App.set_data(app, subject)


class App(tk.Tk):
    '''Главный класс визуального интерфейса'''

    def __init__(self):
        super().__init__()
        self.title("Весы")
        self.geometry("1000x600+120+20")
        self.minsize(800, 500)

        #Camera
        self.vid = cv2.VideoCapture(0)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.open_camera)
        self.thread.start()

        #Mainframe
        self.mainframe = Frame(self)
        self.mainframe.pack(expand=1, fill=tk.BOTH)
        
        # Main menu
        self.mainmenu = Menu(self.mainframe)
        self.config(menu=self.mainmenu)
        
        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label="Открыть...", command=self.open_camera)
        #self.filemenu.add_command(label="Новый")
        #self.filemenu.add_command(label="Сохранить...")
        self.filemenu.add_command(label="Выход", command=self.onClose)
        
        self.helpmenu = Menu(self.mainmenu, tearoff=0)
        #self.helpmenu.add_command(label="Помощь")
        self.helpmenu.add_command(label="О программе", command=self.about)
        
        self.mainmenu.add_cascade(label='Файл', menu=self.filemenu)
        self.mainmenu.add_cascade(label='Справка', menu=self.helpmenu)
        
        # Frames
        self.frame1 = Frame(self.mainframe, bg='red', bd=1)
        self.frame2 = Frame(self.mainframe, bg='blue', bd=1)
        self.frame1.pack(side=TOP, fill='x')
        self.frame2.pack(expand=1, side=TOP, fill='both')
        
        #Image camera
        img = ImageTk.PhotoImage(Image.open("no-image.png").resize((320, 240)))
        self.label = Label(self.frame1, image = img)
        self.label.image = img
        self.label.pack(side=LEFT)

        # Button photo
        self.btn_photo = Button(self.frame1, text="Сделать фото", width=50, command=self.make_photo)
        self.btn_photo.pack(anchor=CENTER, expand=True)

        self.btn_run = Button(self.frame1, text="Запустить тест", width=50, command=self.run_test)
        self.btn_run.pack(anchor=CENTER, expand=True)
        
        # Table
        cols = ('Дата', 'Нетто', 'Брутто', 'Тара', 'Направление')
        self.listBox = ttk.Treeview(self.frame2, columns=cols, show='headings')
        # set column headings
        for col in cols:
            self.listBox.heading(col, text=col)    
        #self.listBox.grid(row=1, column=0, columnspan=2)
        self.listBox.pack(expand=1, fill='both')
        
        # Statusbar
        self.frame_stat = Frame(self)
        #self.statusbar = StatusBar(self.frame)
        self.statusbar = Label(self.frame_stat, text="bigvik © 2023 on the way…", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)
        self.frame_stat.pack(side=tk.BOTTOM, fill=tk.X)

        #Set loggin to statusbar
        lbl_handler = LabelLogging(self.statusbar)
        #lbl_handler.setLevel(logging.INFO)
        lbl_format = logging.Formatter('[%(levelname)s] - %(message)s - (%(asctime)s)')
        lbl_handler.setFormatter(lbl_format)
        logger.addHandler(lbl_handler)

    def run_test(self):
        '''Запускает тест'''
        
        th = threading.Thread(target=control.read_serial)
        th.start()
        th1 = threading.Thread(target=control.write_serial)
        th1.start()

    def open_camera(self):
        '''Видео с камеры'''

        _, self.frame = self.vid.read()
        opencv_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image).resize((320, 240))
        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)
        # Displaying photoimage in the label
        self.label.photo_image = photo_image
        # Configure image in the label
        self.label.configure(image=photo_image)
        # Repeat the same process after every 10 seconds
        self.label.after(10, self.open_camera)

    def make_photo(self):
        '''Сохранить фото с камеры'''

        dt = datetime.datetime.now().strftime('%d.%m.%Y %H.%M.%S')
        cv2.imwrite(f"photo/{dt}.jpg", self.frame)
        logger.info(f'Фото "{dt}.jpg" сохранено')

    def set_data(self, data):
        '''Заполнение таблицы полученными значениями'''

        self.listBox.insert("", "end", values=data)

    def about(self):
        messagebox.showinfo("О программе","bigvik © 2023 on the way…")

    def onClose(self):
        self.stopEvent.set()
        self.quit()


if __name__ == "__main__":
    app = App()
    lis = ViewListener()
    control.observer.attach(lis)
    app.mainloop()