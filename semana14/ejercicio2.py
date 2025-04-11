"""
2. Cree una estructura de objetos que asemeje un Double Ended Queue.
    1. Debe incluir los métodos de `push_left` y `push_right` 
       (para agregar nodos al inicio y al final) y `pop_left` y 
       `pop_right` (para quitar nodos al inicio y al final).
    2. Debe incluir un método para hacer `print` de toda la estructura.
    3. No se permite el uso de tipos de datos compuestos 
       como `lists`, `dicts` o `tuples` ni módulos como `collections`.
"""



class Node:
    """Defines a single node in the queue."""
    def __init__(self, data):
        self.data = data
        self.next = None
        
    def __str__(self):
        return f"Node: {self.data}."


class DoubleEndedQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def push_left(self, node):
        # Add nodes to the beginning=head=left
        if self.tail is None:
            self.tail = node
        node.next = self.head
        self.head = node

    def push_right(self, node):
        # Add nodes to the end=tail=right
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def pop_left(self):
        # Remove nodes to the beginning
        if self.head is None:
            return None
        # Data structure: Node: Third <==> Node: First <==> Node: Fourth <==> Node: Second
        # `self.head` is Third
        # `remove_node` will removed Third node
        remove_node = self.head
        # `self.head` now becomes First
        self.head = self.head.next
        return remove_node.data
    
    def pop_right(self):
        # Remove nodes to the end
        # I need to validate queue is empty.
        # Taking into account that head has track of all the nodes.
        if self.head is None:
            # Queue is empty
            return None
        # If head and tail are the same, it means there is only one node
        # in the queue to be removed.
        if self.head == self.tail:
            # Only one element in the queue.
            # If this is the case, then I need the node to set both
            # head and tail as None to empty the queque.
            only_one_node = self.tail.data
            self.head = None
            self.tail = None
            return only_one_node
        # If both conditions above are NOT matched
        # Then I need to compare if current node is NOT equal to node save in tail
        current_node = self.head
        while current_node.next != self.tail:
            #print(f"Current node: {current_node.data} - {current_node.next}")
            #print(f"Tail: {self.tail.data}")
            # If there is one that matched then it means that
            # I found the one I need to pop from the queue.
            # Then I need to make sure I call next node
            # to get the tail node in the data structure.
            current_node = current_node.next
        # Node in `self.tail` which was found a matched
        # so `current_node` will hold previous element than the one in `self.tail` 
        # Node in `self.tail` is now saved in remove_node to be deleted.
        remove_node = self.tail
        # Here we replace last element with None
        # Data structure: Node: Third <==> Node: First <==> Node: Fourth <==> Node: Second
        # `current_node.next` will be Second, and it is reset or replace for None
        # New Data structure: Node: Third <==> Node: First <==> Node: Fourth
        current_node.next = None
        # `self.tail` now becomes Fourth
        self.tail = current_node
        return remove_node.data

    def print_structure(self, action):
        action = "Pushing nodes" if action == "push" else "Popping node"
        print(f"\n{action} in the queue:")
        if self.head is None:
            print("There are not nodes in the queue.")
            return
        current_node = self.head
        while current_node:
            print(f"Node: {current_node.data}", end=f" == " if current_node.next else "\n")
            current_node = current_node.next


if __name__ == "__main__":
    queue = DoubleEndedQueue()

    # Pushing Nodes
    queue.push_left(Node("First"))
    queue.push_left(Node("Third"))
    queue.push_right(Node("Fourth"))
    queue.push_right(Node("Second"))
    queue.print_structure("push")

    # Popping Nodes
    queue.pop_left()
    queue.print_structure("pop")
    queue.pop_right()
    queue.print_structure("pop")
    queue.pop_left()
    queue.print_structure("pop")
    queue.pop_right()
    queue.print_structure("pop")
