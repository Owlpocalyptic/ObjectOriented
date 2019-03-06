class Observable:
    def __init__(self):
        self.observers = []

    def append_observer(self, o):
        self.observers.append(o)

    def remove_observer(self, o):
        self.observers.remove(o)

    def notify_observers(self):
        for o in self.observers:
            o.receive(self)


class Observer:
    def receive(self):
        raise NotImplementedError()

class