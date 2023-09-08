'''Основной модуль. Controller'''


from __future__ import annotations
import serial

import time
import datetime


import cv2
from abc import ABC, abstractmethod
from typing import List
import logging


logger = logging.getLogger(__name__)
# Create handlers
s_handler = logging.StreamHandler()
f_handler = logging.FileHandler('control.log')
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

import app.config as config
import app.model as model
import app.view as view

ds = model.Datasaver(0)


class Observer(ABC):

	'''Абстрактный оповещатель'''

	@abstractmethod
	def attach(self, observer) -> None:
		pass

	@abstractmethod
	def detach(self, observer) -> None:
		pass

	@abstractmethod
	def notify(self) -> None:
		pass


class ExecutiveObserver(Observer):
	'''Конкретный оповещатель обновлений'''
	
	_msg: str = ''
	_observers: List = []
	_weight : List = []

	def attach(self, observer) -> None:
		self._observers.append(observer)

	def detach(self, observer) -> None:
		self._observers.remove(observer)

	def notify(self) -> None:
		for observer in self._observers:
			observer.update(self._weight)
		self._weight = []

	def send_msg(self) -> None:
		for observer in self._observers:
			observer.message(self._msg)
		self._msg = ''

	def set_changes(self, weight) -> None:
		self._weight = weight
		self.notify()

	def set_msg(self, msg) -> None:
		self._msg = msg
		self.send_msg()


observer = ExecutiveObserver()


def prepare(l:list) -> list:
    return [datetime.datetime.now().strftime('%d.%m.%Y %H.%M.%S'),
              abs(l[0]-l[1]),
              max(l),
              min(l),
              'IN' if l[0]>l[1] else 'OUT']


def write_serial() -> None:
    with serial.Serial() as ser:
        ser.port = 'COM4'
        ser.baudrate = 9600
        ser.open()
        with open("test/log_brutto.txt", "rb") as f:
            while (byte := f.read(8)):
                ser.write(byte)
        time.sleep(1)
        with open("test/log_netto.txt", "rb") as f:
            while (byte := f.read(8)):
                ser.write(byte)


def read_serial() -> None:
    c = 1
    d = {}
    e = []
    with serial.Serial() as ser:
        ser.port = config.PORT
        ser.baudrate = config.BAUD
        ser.open()
        config.logger.info(f'Запущено прослушивание порта: {config.PORT}')
        while True:
            bs = int(ser.read(8)[::-1][:-1])
            if bs != 0:
                if d == {}:
                    config.logger.info(f'Начато {c} измерение')
                    view.app.make_photo()
                if d.get(bs):
                    d[bs] = d[bs] + 1
                else:
                    d[bs] = 1
            elif bs == 0 and d != {}:  
                e.append(max(d, key=d.get))
                d.clear()
                if c == 1:
                    c+=1
                    #print(f'Waiting mesurement {c}...')
                else:
                    c = 1
                    save_data(prepare(e))
                    e.clear()


def make_foto(name: str) -> None:

	'''Делает фото взвешиваемого автомобиля'''
	
	stream = cv2.VideoCapture('rtsp://login:password@IP/')
	r, f = stream.read()
	path = f"photo/{name}.jpg"
	cv2.imwrite(path, f)
	logger.info(f'Photo: {path}')


def preparation_data(weight: list) -> tuple:

	'''Подготавливает полученые данные для сохранения.
	Получает список из двух элементов. Возвращает tuple из пяти'''

	dt = datetime.datetime.now().strftime('%d.%m.%Y %H.%M.%S')
	netto = weight[0] - weight[1]
	if netto == 0: return ()
	if netto > 0:
		return (dt, weight[0], netto, weight[1], 'IN')
	else:
		return (dt, weight[1], abs(netto), weight[0], 'OUT')


def save_data(data: list):

	'''Сохраняет данные через Datasaver.
	Анонсирует изменения для Слушателей'''

	#ds.set_data(preparation_data(weight))
	ds.save_data(data)
	observer.set_changes(data)
	observer.set_msg('Сохранение данных')


def open_serial():
	observer.set_msg('Подключение к порту')
	try:
		ser = serial.Serial(
				port = 'COM5',
				baudrate = 9600,
				bytesize = 8,
				parity = 'N',
				stopbits = 1,
				timeout = 1,
				xonxoff = 0,
				rtscts = 0,
				#interCharTimeout = 1,
				writeTimeout = 1)
		while True:
			if ser.inWaiting() > 0:
				get_weight(ser)
			time.sleep(1)
	except OSError:
		observer.set_msg('ОШИБКА: Нет подключения к порту')


def rule_lamp():

	'''Через реле включает и выключает лампочку'''

	lamp = serial.Serial(
		port = 'COM7',
		baudrate = 9600,
		bytesize = 8,
		parity='N',
		stopbits = 1,
	)
	lamp.write(b'\x01\x05\x00\x00\xFF\x00\x8C\x3A') #включение
	time.sleep(7)
	lamp.write(b'\x01\x05\x00\x00\x00\x00\xCD\xCA') #выключение


def end_weighting(w: int) -> None:

	'''Вызывается при завершении взвешивания'''

	observer.set_msg('Конец взвешивания')
	logger.info(f'Конец взвешивания: ({w})')
	dt = datetime.datetime.now().strftime('%d.%m.%Y %H.%M.%S')
	name = f'{dt} - ({w})'
	make_foto(name)
	rule_lamp()


def get_weight(ser):
	
	'''Базовая функция для измерения веса. Редактируется только SV4618'''

	observer.set_msg('Начало взвешивания')
	logger.info('Начало взвешивания')
	weight_list = []
	try:
		while True:
			weight = ser.readline(8)
			
			if weight > b'=0000000':

				#for i in range(4):
				#	tmp_weight = int(str((ser.readline(8)[::-1][:-1]).decode("utf-8")))
				#	if tmp_weight == weight: continue

				weight1 = ser.readline(8)
				if weight1 == weight:
					weight2 = ser.readline(8)
					if weight2 == weight:
						weight3 = ser.readline(8)
						if weight3 == weight:
							weight4 = ser.readline(8)
							if weight4 == weight:
								weight5 = ser.readline(8)
								if weight5 == weight:
									ser.close()
									time.sleep(3)
									ser.open()
									weight6 = ser.readline(8)
									if weight6 == weight5:
										weight7 = abs(int(str((ser.readline(8)[::-1][:-1]).decode("utf-8"))))
										weight_list.append(weight7)
										end_weighting(weight7)

										if len(weight_list) == 2:

											save_data(weight_list)

											try:
												while not int(str((ser.readline(8)[::-1][:-1]).decode("utf-8"))) == 0:
													ser.close()
													open_serial()
											except UnicodeDecodeError as err:
												print(err)
												ser.close()
												time.sleep(2)
												ser.open()
												pass
											except ValueError as er:
												print(er)
												ser.close()
												time.sleep(2)
												ser.open()
												pass
										try:
											while not int(str((ser.readline(8)[::-1][:-1]).decode("utf-8"))) == 0:
												pass										
										except UnicodeDecodeError as err:
											print(err)
											ser.close()
											time.sleep(2)
											ser.open()
											pass
										except ValueError as er:
											print(er)
											ser.close()
											time.sleep(2)
											ser.open()
											pass
	except UnicodeDecodeError as err:
		print(err)
		ser.close()
		time.sleep(2)
		ser.open()
		pass
	except ValueError as er:
		print(er)
		ser.close()
		time.sleep(2)
		ser.open()
		pass


if __name__ == "__main__":
	open_serial()