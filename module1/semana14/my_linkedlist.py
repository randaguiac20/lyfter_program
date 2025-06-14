

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
        
class LinkedList:
    def __init__(self, head):
        self.head = head
        
    def print_node(self):
        current_node = self.head
        if current_node is None:
            print("There are not nodes in the queue.")
            return
        while current_node is not None:
            print(f"Node: {current_node.data}", end=" ==> " if current_node.next else "\n")
            current_node = current_node.next

tnode = Node("third")
snode = Node("second", tnode)
fnode = Node("first", snode)

queue = LinkedList(fnode)
queue.print_node()