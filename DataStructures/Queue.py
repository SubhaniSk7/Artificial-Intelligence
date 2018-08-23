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


# ----------------------------------------------
# Singly LinkedList Implementation

class Queue:

    def __init__(self, data=None):
        self.head = None;  # self.front=None
        # self.last = None;  # self.rear=None
        self.length = 0;

    def enqueue(self, data):

        newNode = Node(data);

        if (self.head is None):
            self.head = newNode;
        else:
            temp = self.head;
            while (temp.getNext() != None):
                temp = temp.getNext();
            temp.setNext(newNode);
        self.length += 1;

    def dequeue(self):
        if (self.head is None):
            print('queue is empty..');
            return None;

        temp = self.head;
        self.head = temp.getNext();
        self.length -= 1;
        return temp;

    def queueLength(self):
        return self.length;

    def printQueue(self):

        if (self.head != None):
            temp = self.head;
            print();
            while (temp != None):
                print(temp.data, end=' ');
                temp = temp.getNext();
        else:
            print('queue is empty..');


# ------------------------------


queue = Queue();

while (True):

    print('-----------------------');
    print('1.enqueue\n2.dequeue\n3.print\n4.length\n5.exit');
    print('-----------------------');

    choice = int(input('enter choice:'));
    if (choice == 1):
        ele = int(input('enter data:'));
        queue.enqueue(ele);
    elif (choice == 2):
        print(queue.dequeue().data);
    elif (choice == 3):
        queue.printQueue();
        print();
    elif (choice == 4):
        print(queue.queueLength());
    elif (choice == 5):
        break;
