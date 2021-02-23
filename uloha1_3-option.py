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
    #Poslednym a zaroven najefektivnejsim bolo pridanie locku este pred while.
    #Kedze je zamok uzamknuty, druhe vlakno musi cakat na dokoncenie toho vlakna,
    #ktore ho uzamklo. Nedochazda tu k spomaleniu kvoli cyklu,
    #kedze vlakno caka este pred nim. Z pohladu paralelneho je toto riesenie asi nu-li-tne (teda pokial to dobre chapem)
    #Ospravedlnujem sa, ako to je hodene na github
    #no musim sa s tym naucit nejako robit. Nabuduce to snad bude lepsie.
    shared.mutex.lock()
    while True:
        if shared.counter >= shared.end:
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
