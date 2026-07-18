# Queue class definition used for storing user performance
class Queue:
    # Class constructor with contents on queue and its maximum size (always 20)
    def __init__(self):
        self.contents = []
        self.max_size = 20

    def dequeue(self):
        '''Method to dequeue fromt item in queue'''
        self.contents.pop(0)    

    def enqueue(self, item):
        '''Method to add item to end of queue'''
        if self.is_full():
            # If queue is at maximum size dequeue front item first
            self.dequeue()
        self.contents.append(item)

    def size(self):
        '''Method to return current number of items in queue'''    
        return len(self.contents)
    
    def is_full(self):
        '''Method to check is queue is at maximum size'''
        return self.size() == self.max_size
    
    def get_queue(self):
        '''Method used to return contents of queue to the main program as a list'''
        return self.contents
