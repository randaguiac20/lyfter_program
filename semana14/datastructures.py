

class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
        
class DataStructure:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
    
    def enqueue(self, node):
        if self.head is None:
            self.head = node
            return
        current_node = self.head
        while current_node.next_node is not None:
            current_node = current_node.next_node
        current_node.next_node = node
    
    def dequeue(self):
        if self.head is None:
            return None
        remove_node = self.head.data
        self.head = self.head.next_node
        return remove_node
        
    def push_left(self, node):
        if self.head is None:
            self.tail = node
        node.next_node = self.head
        self.head = node
    
    def push_right(self, node):
        if self.head is None:
            self.head = self.tail = node
            return self.tail
        self.tail.next_node = node
        self.tail = node
    
    def pop_left(self):
        if self.head is None:
            return None
        remove_node = self.head.data
        self.head = self.head.next_node
        return remove_node
    
    def pop_right(self):
        if self.head is None:
            return None
        if self.tail == self.head:
            remove_node = self.tail.data
            self.head = self.tail = None
            return remove_node
        current_node = self.head
        while current_node.next_node != self.tail:
            current_node = current_node.next_node
        remove_node = self.tail.data
        current_node.next_node = None
        self.tail = current_node
        return remove_node

    def print_linkedlist(self):
        if self.head is None:
            print("Queue is empty.")
            return
        current_node = self.head
        print()
        while current_node is not None:
            print(f"Node: {current_node.data}", end=" ==> " if current_node.next_node else "\n")
            current_node = current_node.next_node
        print()
    
    def print_queue(self):
        if self.head is None:
            print("\nQueue is empty.\n")
            return
        current_node = self.head
        print()
        while current_node is not None:
            print(f"Node: {current_node.data}", end=" ==> " if current_node.next_node else "\n")
            current_node = current_node.next_node
        print()
    
    def print_stak(self):
        if self.head is None:
            print("\nQueue is empty.\n")
            return
        current_node = self.head
        print()
        while current_node is not None:
            print(f"Node: {current_node.data}", end=" ==> " if current_node.next_node else "\n")
            current_node = current_node.next_node
        print()
    
    def print_dendedqueue(self):
        if self.head is None:
            print("\nQueue is empty.\n")
            return
        current_node = self.head
        print()
        while current_node is not None:
            print(f"Node: {current_node.data}", end=" ==> " if current_node.next_node else "\n")
            current_node = current_node.next_node
        print()
    
    def print_binaytree(self):
        pass
    
    def print_circular(self):
        pass
    

# LinkedList logic
# print("LinkedList logic")
# ds = DataStructure()
# ds.enqueue(Node("first"))
# ds.enqueue(Node("second"))
# ds.enqueue(Node("third"))
# ds.print_linkedlist()

# Queue logic
# print("\nQueue logic")
# ds = DataStructure()
# print("\n ==> Enqueue node")
# ds.enqueue(Node("first"))
# ds.enqueue(Node("second"))
# ds.enqueue(Node("third"))
# ds.print_queue()
# print("\n ==> Dequeue node")
# ds.dequeue()
# ds.print_queue()
# ds.dequeue()
# ds.print_queue()
# ds.dequeue()
# ds.print_queue()

# Stack logic
# print("\nStack logic")
# ds = DataStructure()
# print("\n ==> Push node")
# ds.push_right(Node("first"))
# ds.push_right(Node("Second"))
# ds.push_right(Node("Third"))
# ds.print_stak()
# print("\n ==> Pop node")
# ds.print_stak()
# ds.pop_right()
# ds.print_stak()
# ds.pop_right()
# ds.print_stak()
# ds.pop_right()
# ds.print_stak()

# Double Ended Queue logic
print("\nDouble Ended Queue logic")
ds = DataStructure()
print("\n ==> Push node")
ds.push_left(Node("First"))
ds.push_left(Node("Second"))
ds.push_right(Node("Third"))
ds.push_right(Node("Forth"))
ds.print_dendedqueue()
print("\n ==> Pop node")
ds.print_dendedqueue()
ds.pop_left()
ds.print_dendedqueue()
ds.pop_left()
ds.print_dendedqueue()
ds.pop_right()
ds.print_dendedqueue()
ds.pop_right()
ds.print_dendedqueue()


# Binary Tree logic


# Circular logic


