from threading import Thread


class ThreadWithReturnValue(Thread):
    # https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def wait_result(self, *args):
        Thread.join(self, *args)
        return self._return

    def last_result(self):
        return self._return

