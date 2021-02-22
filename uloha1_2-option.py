from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


def counter(shared):
    while True:
        #druhym napadom bolo premiestnit lock este pred kontrolu stavu, ci uz sme na
        #konci pola, aby sme predisli predchadzajucej chybe out of range.
        #Tu uz sme boli uspesni, nakolko aj pri pokuse s 10_000_000 boli vsetky
        #hotnoty v liste 1
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


for _ in range(10):
    sh = Shared(10_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array))
