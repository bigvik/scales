'''Модуль для тестов'''

import control
import time

def timer(function):
    '''
    Функция декоратор для измерения времени выполнения функции
    '''
    def wrapped(*args):
        start_time = time.perf_counter()
        res = function(*args)
        print(time.perf_counter() - start_time)
        return res
    return wrapped

@timer   
def test():
    print('Test')
    for x in range(5):
        control.save_data([x, 100])

def test_observer():
    
    control.anons.set_msg('Тестирование')
    for x in range(100,0,-20):
        for y in range(0,100,20):
            control.save_data([x, y])
    control.anons.set_msg('Конец теста')

def test_bot():
    control.anons.set_msg('Тестирование BOT')
    for x in range(100,0,-20):
        control.save_data([100, x])
        time.sleep(1)
    control.anons.set_msg('Конец теста')

if __name__=='__main__':
    test()