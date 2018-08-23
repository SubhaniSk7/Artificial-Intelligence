class Node:

    # data=None;
    # next=None;

    # constructor
    def __init__(self, data=None):
        self.data = data;
        self.next = None;

    def setData(self, data):
        self.data = data;

    def getData(self):
        return self.data;

    def setNext(self, next):
        self.next = next;

    def getNext(self):
        return self.next;