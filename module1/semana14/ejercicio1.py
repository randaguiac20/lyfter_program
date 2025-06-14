"""
1. Cree una estructura de objetos que asemeje un Stack.
    1. Debe incluir los métodos de `push` (para agregar nodos)
       y `pop` (para quitar nodos).
    2. Debe incluir un método para hacer `print` de toda la estructura.
    3. No se permite el uso de tipos de datos compuestos 
       como `lists`, `dicts` o `tuples` ni módulos como `collections`.
    
STACK == LIFO (Last In First Out)

- Se basa en las Linked Lists.
- Tiene un nodo `top`.
- `LIFO`: Last In, First Out
    - El ultimo `nodo` que entre es el primero que sale.
    - Como cuando uno tiene una pila de discos y quiere sacar uno que está en medio. Debe sacar todos los que puso después de ese para poder sacarlo.
- Tiene dos métodos:
    - `push` para agregar `nodos`  (al inicio).
    - `pop` para quitar `nodos` (del inicio).

>> Example to understand Stack concept

stack = []
stack.append(10)  # Push 10
stack.append(20)  # Push 20
stack is equal to [10, 20]
stack.pop()       # Pop (removes 20 the last element)

"""

class Node:
    """Defines a single node in the stack."""
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def push(self, node):
        node.next = self.head
        self.head = node

    def pop(self):
        if self.head is None:
            return None
        remove_node = self.head
        self.head = self.head.next
        return remove_node.data

    def print_structure(self, action):
        action = "Pushing nodes" if action == "push" else "Popping node"
        print(f"\n{action} in the Stack: ")
        if self.head is None:
            print("No more nodes in the Stack.")
            return
        current_node = self.head
        while current_node:
            print(f"Node: {current_node.data}", end=f" ==> " if current_node.next else "\n")
            current_node = current_node.next


if __name__ == "__main__":
    stack = Stack()

    # Pushing Nodes
    stack.push(Node("First"))
    stack.push(Node("Second"))
    stack.push(Node("Third"))
    stack.push(Node("Fourth"))
    stack.print_structure("push")

    # Popping Nodes
    stack.pop()
    stack.print_structure("pop")
    stack.pop()
    stack.print_structure("pop")
    stack.pop()
    stack.print_structure("pop")
    stack.pop()
    stack.print_structure("pop")
