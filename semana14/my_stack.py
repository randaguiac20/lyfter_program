

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
        
class LinkedList:
    
    def __init__(self, head):
        self.head = head
        
    def print_queue(self):
        current_node = self.head
        while current_node:
            print(f"Node: {current_node.data}", end=" ==> " if current_node.next else "\n")
            current_node = current_node.next
            
class Stack(LinkedList):
    def push(self, current_node):
        # FIRST iteration workflow calling push
        current_node.next = self.head # self.head == 0
        self.head = current_node # self.head == 1
        # node: first ==> node: cero
    
    def pop(self):
        if self.head:
            self.head = self.head.next



print("\n ==> Push nodes\n")
node = Node("Cero")
stack = Stack(node)
node = Node("first")
stack.push(node)
node = Node("Second")
stack.push(node)
stack.print_queue()

print("\n ==> Pop nodes\n")
stack.print_queue()
stack.pop()
stack.print_queue()
stack.pop()
stack.print_queue()
stack.pop()
stack.print_queue()
