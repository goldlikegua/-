#***************************简单装饰器********************************
def debug(func):
    def wrapper():
        print('DEBUG: {}'.format(func.__name__))
        return func()
    return wrapper

@debug
def fun():
    print('hello')

#fun()
'''
DEBUG: fun
hello
'''

#***************************带参数装饰器********************************
def logging(level):
    def outwrapper(func):
        def wrapper(*args, **kwargs):
            print('[{0}]: enter {1}()'.format(level, func.__name__))
            return func(*args, **kwargs)
        return wrapper
    return outwrapper

@logging('INFO')
def hello(a, b, c):
    print(a + ',' + b + ',' + c)


#hello('hello','good','night')
'''
[INFO]: enter hello()
hello,good,night
'''
#***************************类装饰器********************************
class logging(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print('[DEBUG]: enter {}()'.format(self.func.__name__))
        return self.func(*args, **kwargs)

@logging
def hello(a, b, c):
    print(a + ',' + b + ',' + c)

# hello('hello','good','night')

#**********************带参数的类装饰器******************************
class loggings(object):
    
    def __init__(self, level):
        self.level = level
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print('[{}]: enter {}()'.format(self.level, func.__name__))
            return func(*args, **kwargs)
        return wrapper

@loggings('leveling')
def hello(a, b, c):
    print(a + ',' + b + ',' + c)

# hello('hello','good','night')

#**************************实验*********************************
def timeRunning(func):
    def wrapper(*args, **kwargs):
        import time
        T1 = time.time()
        res = func(*args, **kwargs)
        T2 = time.time()
        print('{}函数运行的时间为：{}'.format(func.__name__, T2 - T1))
        return res
    return wrapper

@timeRunning    
def func(a, b):
    res = 0
    for i in range(a, b*10):
        res += i
    return res

func(1, 10000)