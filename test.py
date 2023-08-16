import control
import time

def timer(function):
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
    print('Test Observer')
    for x in range(5):
        control.save_data([x, 100])
        time.sleep(3)

if __name__=='__main__':
    test()