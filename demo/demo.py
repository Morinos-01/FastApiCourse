def func_def(*args, **kwargs):
    def wraps(func):
        def inner(*args, **kwargs):
            print("хаюхай")
            res = func(*args, **kwargs)
            print("пока")
            return res
        return inner
    return wraps


@func_def()
def one_plus(a, b):
    print(a + b)


one_plus(1, 2)