"""
3. Cree una estructura de objetos que asemeje un Binary Tree.
    1. Debe incluir un método para hacer `print` de toda la estructura.
    2. No se permite el uso de tipos de datos compuestos 
       como `lists`, `dicts` o `tuples` ni módulos como `collections`.
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class QueueNode:
        def __init__(self, node):
            self.node = node
            self.next = None


class QueueManager:
    def __init__(self):
        self.left = None
        self.right = None

    def add(self, node):
        new_node = QueueNode(node)
        if self.right:
            self.right.next = new_node
        else:
            self.left = new_node
        self.right = new_node
        
    def remove(self):
        if self.left is None:
            return None
        new_node = self.left.node
        self.left = self.left.next
        if self.left is None:
            self.right = None
        return new_node
    
    def current_node(self):
        if self.left:
            print(f"Current Node: {self.left.node.data}")
            return self.left.node
        return None

    @property
    def is_empty(self):
        if self.left is None:
            return None


class BinaryTree:
    def __init__(self, root_node, queue):
        self.root = root_node
        self.queue = queue
        self.queue.add(self.root)

    def insert(self, node):
        print(f"\n================ Inserting {node.data} ================")
        while not self.queue.is_empty:
            # current_node = self.queue.remove()
            current_node = self.queue.current_node()
            print(f"\n===> Visiting Node {current_node.data}")
            if current_node.left is None:
                current_node.left = node
                print(f"Inserted {node.data} to the LEFT of {current_node.data}")
                self.queue.add(node)  # Node might accept children in the future
                return
            if current_node.right is None:
                current_node.right = node
                print(f"Inserted {node.data} to the RIGHT of {current_node.data}")
                self.queue.add(node)
                self.queue.remove()  # Current node now has 2 children
                return
            # if not current_node.left:
            #     print("Left")
            #     current_node.left = node
            #     print(f"Inserted {node.data} to the LEFT of {current_node.data}")
            #     return
            # else:
            #     print("Left")
            #     print(f"{current_node.data} already has LEFT child {current_node.left.data}")
            #     self.queue.add(current_node.left)

            # if not current_node.right:
            #     print("Right")
            #     current_node.right = node
            #     print(f"Inserted {node.data} to the RIGHT of {current_node.data}")
            #     return
            # else:
            #     print("Right")
            #     print(f"{current_node.data} already has RIGHT child {current_node.right.data}")
            #     self.queue.add(current_node.right)

    def print_structure(self, node=None, level=0, prefix="\nRoot-- "):
        if node is None:
            node = self.root
        print("  " * level + prefix + str(node.data))

        if node.left:
            self.print_structure(node.left, level + 1, "L--- ")
        if node.right:
            self.print_structure(node.right, level + 1, "R--- ")

    

root_node = Node(1)
queue = QueueManager()
tree = BinaryTree(root_node, queue)

for node in range(2, 18):
    tree.insert(Node(node))

tree.print_structure()
