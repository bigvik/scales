'''Основной модуль. Controller'''


from __future__ import annotations
import serial

import time
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
#import snoop
import os
import smtplib
import cv2
from abc import ABC, abstractmethod
from typing import List



import model

ds = model.Datasaver(0)

class Subject(ABC):

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


class Annunsiator(Subject):

	'''Конкретный оповещатель обновлений'''
	
	_state: int = 0
	_msg: str = ''
	_observers: List = []
	_weight : List = []

	def attach(self, observer) -> None:
		self._observers.append(observer)

	def detach(self, observer) -> None:
		self._observers.remove(observer)

	def notify(self) -> None:

		for observer in self._observers:
			observer.update(self)
		print('Notify')

	def set_changes(self, weight) -> None:
		print('Annunsiator set changes')
		self._state += 1
		self._weight = weight
		print(f'{self._state} -> {self._weight}')
		self.notify()

	def set_msg(self, msg):
		self._msg = msg
		self.notify()


anons = Annunsiator()

def print_doc():
	os.startfile(r"c:\Users\Kolomna\Documents\SV\Vesy\Print_doc.xlsx", 'print')


def make_foto(dt):

	'''Делает фото взвешиваемого автомобиля'''
	
	stream = cv2.VideoCapture('rtsp://login:password@IP/')
	r, f = stream.read()
	path = f"photo/{dt}.jpg"
	cv2.imwrite(path, f)


def preparation_data(weight:list) -> tuple:

	'''Подготавливает полученые данные для сохранения.
	Получает список из двух элементов. Возвращает tuple из пяти'''

	dt = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
	netto = weight[0] - weight[1]
	if netto > 0:
		return (dt, weight[0], netto, weight[1], 'IN')
	else:
		return (dt, weight[1], abs(netto), weight[0], 'OUT')


def save_data(weight):

	'''Сохраняет подготовленные в preparation_data данные через Datasaver.
	Анонсирует изменения для Слушателей'''

	ds.set_data(preparation_data(weight))
	ds.save_data()
	anons.set_changes(preparation_data(weight))
	anons.set_msg('Сохранение данных')

#@snoop
def open_serial():
	anons.set_msg('Подключение к порту')
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
		pass


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


def end_weighting():

	'''Вызывается при завершении взвешивания'''

	anons.set_msg('Конец взвешивания')
	dt = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
	make_foto(dt)
	rule_lamp()

#@snoop
def get_weight(ser):
	
	'''Базовая функция для измерения веса. Редактируется только SV4618'''

	anons.set_msg('Начало взвешивания')
	weight_list = []
	try:
		while True:
			weight = int(str((ser.readline(8)[::-1][:-1]).decode("utf-8")))
			
			if weight > 0:

				#for i in range(4):
				#	tmp_weight = int(str((ser.readline(8)[::-1][:-1]).decode("utf-8")))
				#	if tmp_weight == weight: continue

				weight1 = abs(int(str((ser.readline(8)[::-1][:-1]).decode("utf-8"))))
				if weight1 == weight:
					weight2 = int(str((ser.readline(8)[::-1][:-1]).decode("utf-8")))
					if weight2 == weight:
						weight3 = int(str((ser.readline(8)[::-1][:-1]).decode("utf-8")))
						if weight3 == weight:
							weight4 = int(str((ser.readline(8)[::-1][:-1]).decode("utf-8")))
							if weight4 == weight:
								weight5 = int(str((ser.readline(8)[::-1][:-1]).decode("utf-8")))
								if weight5 == weight:
									ser.close()
									time.sleep(3)
									ser.open()
									weight6 = int(str((ser.readline(8)[::-1][:-1]).decode("utf-8")))
									if weight6 == weight5:

										weight_list.append(weight6)
										end_weighting()

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