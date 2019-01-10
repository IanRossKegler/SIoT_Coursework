def increment_counter():
    f = open('counter.txt')
    count = int(f.readline())
    f.close()
    f = open('counter.txt', 'w')
    count += 1
    f.write(str(count))
    f.close()


def read_counter():
    f = open('counter.txt')
    count = int(f.readline())
    f.close()
    return count


def reset_counter():
    f = open('counter.txt', 'w')
    f.write(str(0))
    f.close()
