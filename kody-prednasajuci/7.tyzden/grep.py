import sys


def cat(file, gen):
    for line in file:
        gen.send(line)
    gen.close()


def grep(substring, gen):
    try:
        while True:
            line = yield
            gen.send(line.count(substring))
    except GeneratorExit:
        gen.close()


def wc(substring):
    n = 0
    try:
        while True:
            n += yield
    except GeneratorExit:
        print(substring, n)


def main():
    if len(sys.argv) != 3:
        print('usage: grep.py string file')
        sys.exit(-1)
    file = open(sys.argv[2])
    substring = sys.argv[1]

    w = wc(substring)
    next(w)
    g = grep(substring, w)
    next(g)

    cat(file, g)


if __name__ == '__main__':
    main()
