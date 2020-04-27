def fib(limit):
    i = 1
    a, b = 0, 1
    while True:
        if i > limit:
            return
        yield b
        a, b = b, a+b
        i += 1
