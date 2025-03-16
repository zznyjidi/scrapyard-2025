import _thread

try:
    threadLockPool # type: ignore
except NameError:
    threadLockPool = []

def waitForAllLocks():
    global threadLockPool
    while any(map(lambda lock: not lock.locked(), threadLockPool)):
        pass
    for lock in threadLockPool:
        lock.acquire()
        lock.release()

def with_lock(func):
    global threadLockPool
    lock: _thread.LockType = _thread.allocate_lock()
    threadLockPool.append(lock)
    
    def wrapper(*args, **kwargs):
        lock.acquire()
        try:
            func(*args, **kwargs)
        finally:
            lock.release()
    return wrapper
