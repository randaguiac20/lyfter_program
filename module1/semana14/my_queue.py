


class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
        
class LinkedList:
    def __init__(self, head):
        self.head = head
        
    def print_queue(self):
        current_node = self.head
        if current_node is None:
            print("There are not nodes in the queue.")
            return
        while current_node is not None:
            print(f"Node: {current_node.data}", end=" ==> " if current_node.next else "\n")
            current_node = current_node.next

class Queue(LinkedList):
    def enqueue(self, new_node):
        # FIRST iteration workflow calling enqueue
        current_node = self.head # current_node == 0
        while current_node.next is not None: # IN SECOND iteration current_node.next IS NONE
            # THIRD iteration workflow calling enqueue
            current_node = current_node.next # current_node.next == 1
        # SECOND iteration workflow calling enqueue
        # new_node == 1 THEN current_node.next == 1
        # THIRD iteration workflow calling enqueue
        # new_node == 2 THEN current_node.next == 2
        current_node.next = new_node # new_node == 1 THEN current_node.next == 1
        # node: cero ==> node: first ==> node: second
    
    def dequeue(self):
        if self.head:
            self.head = self.head.next
            
    
print("\n>> Enqueue new node\n")
node = Node("Cero")
queue = Queue(node)
node = Node("first")
queue.enqueue(node)
node = Node("second")
queue.enqueue(node)
node = Node("third")
queue.enqueue(node)
node = Node("forth")
queue.enqueue(node)
queue.print_queue()
print("\n>> Dequeue node\n")
queue.print_queue()
queue.dequeue()
queue.print_queue()
queue.dequeue()
queue.print_queue()
queue.dequeue()
queue.print_queue()
queue.dequeue()
queue.print_queue()
