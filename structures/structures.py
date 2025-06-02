class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
    
    def __str__(self):
        return str(self.items)
    
    
    def __repr__(self):
        return str(self)
    
    
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        raise IndexError("dequeue from empty queue")

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        raise IndexError("peek from empty queue")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
    
    def __str__(self):
        return str(self.items)
    
    def __repr__(self):
        return str(self)
    
class PriorityQueue:
    def __init__(self):
        self.items = []

    def add(self, item, priority):
        self.items.append((item, priority))
        self.items.sort(key=lambda x: x[1])

    def remove(self):
        if not self.is_empty():
            return self.items.pop(0)[0]
        raise IndexError("dequeue from empty priority queue")

    def peek(self):
        if not self.is_empty():
            return self.items[0][0]
        raise IndexError("peek from empty priority queue")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
    
    def __str__(self):
        return str([item[0] for item in self.items])
    
    def __repr__(self):
        return str(self)