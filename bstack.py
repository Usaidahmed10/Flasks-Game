'''
Bounded Stack Implementation
Written by : Usaid Ahmed
'''

class BoundedStack:
    def __init__(self, capacity):
        assert isinstance(capacity, int), ('Error: Type error: %s' % (type(capacity))) # throws an assertion error on not true
        assert capacity >= 0, ('Error: Illegal capacity: %d' % (capacity))        
        self.__items = []
        self.__capacity = capacity
    
    def push(self, item):
        if len(self.__items) >= self.__capacity:
            raise Exception('Error: Stack is full')        
        self.__items.append(item)
    
    def pop(self):
        if len(self.__items) == 0:
            raise Exception("The stack is empty")
        return self.__items.pop()
    
    def peek(self):
        if len(self.__items) == 0:
            raise Exception("The stack is empty")        
        return self.__items[len(self.__items)-1] 
    
    def isEmpty(self):
        return self.__items == []
    
    def size(self):
        return len(self.__items)
    
    def show(self):
        print(self.__items)
    
    def __str__(self):
        stackAsString = ''
        for item in self.__items:
            stackAsString += item + ' '
        return stackAsString
    
    def clear(self):
        self.__items.clear()  
        
    def capacity(self):        
        return self.__capacity    
    
    def isFull(self):
        return len(self.__items) == self.__capacity    