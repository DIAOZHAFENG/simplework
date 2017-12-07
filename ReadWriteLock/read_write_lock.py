from threading import Lock


class ReadWriteLock():
    def __init__(self, f):
        self.f = f
        self.rn = 0
        self.r_lock = Lock()
        self.w_lock = Lock()

    def r_acquire(self):
        self.r_lock.acquire()
        if self.rn == 0:
            self.w_lock.acquire()
        self.rn += 1
        self.r_lock.release()

    def r_release(self):
        self.r_lock.acquire()
        self.rn -= 1
        if self.rn == 0:
            self.w_lock.release()
        self.r_lock.release()

    def w_acquire(self):
        self.w_lock.acquire()

    def w_release(self):
        self.w_lock.release()
