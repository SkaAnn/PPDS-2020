import sys


def consumer(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return wrapper


def cat(file, gen):
    for line in file:
        gen.send(line)
    gen.close()


# Pouzitie dekoratora @consumer je to iste ako keby som zavolal
# grep = consumer(grep)
@consumer
def grep(substring, gen):
    try:
        while True:
            line = yield
            gen.send(line.count(substring))
    except GeneratorExit:
        gen.close()


@consumer
def wc(substring):
    n = 0
    try:
        while True:
            n += yield
    except GeneratorExit:
        print(substring, n)


@consumer
def dispatch(greps):
    try:
        while True:
            line = yield
            for g in greps:
                g.send(line)
    except GeneratorExit:
        for g in greps:
            g.close()


def main():
    if len(sys.argv) < 3:
        print('usage: grep.py string... file')
        sys.exit(-1)
    file = open(sys.argv[-1])
    substrings = sys.argv[1:-1]
    greps = []

    for substring in substrings:
        w = wc(substring)
        g = grep(substring, w)
        greps.append(g)

    d = dispatch(greps)
    cat(file, d)


if __name__ == '__main__':
    main()
