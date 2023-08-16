#!/usr/bin/Python

import serial

import time
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
#import snoop
import os
import smtplib
import cv2


import model




def print_doc():
	os.startfile(r"c:\Users\Kolomna\Documents\SV\Vesy\Print_doc.xlsx", 'print')


def make_foto(dt):
	
	stream = cv2.VideoCapture('rtsp://login:password@IP/')
	r, f = stream.read()
	path = f"c:/Users/Kolomna/Documents/SV/Vesy/foto_camera/{dt}.jpg"
	cv2.imwrite(path, f)
	

def send_email(x):
	pass


def preparation_data(weight):

	dt = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
	netto = weight[0] - weight[1]
	if netto > 0:
		return (dt, weight[0], netto, weight[1], 'IN')
	else:
		return (dt, weight[1], abs(netto), weight[0], 'OUT')


def save_data(weight):

	ds = model.Datasaver(0)
	ds.set_data(preparation_data(weight))
	ds.save_data()

#@snoop
def open_serial():
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
	#управление реле
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
	dt = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
	make_foto(dt)
	rule_lamp()

#@snoop
def get_weight(ser):
	#фиксация веса
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