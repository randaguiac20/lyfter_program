class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.next = None  # Used only for internal queueing


class BinaryTree:
    def __init__(self, root):
        self.root = root
        self.queue_head = root  # Acts as queue's front
        self.queue_tail = root  # Acts as queue's rear

    def insert(self, node):
        current_node = self.queue_head
        print(f"\n================ Inserting {node.data} ================")
        print(f"\n===> Visiting Node {current_node.data}")
        # Insert to left if available
        if current_node.left is None:
            current_node.left = node
            print(f"Inserted {node.data} to the LEFT of {current_node.data}")
        # Otherwise insert to right
        elif current_node.right is None:
            current_node.right = node
            print(f"Inserted {node.data} to the RIGHT of {current_node.data}")
            # Move queue head forward (this node is now "full")
            self.queue_head = current_node.next
        else:
            # This shouldn't happen if logic is followed
            raise Exception("Both children already occupied!")

        # Append new node to queue
        self.queue_tail.next = node
        self.queue_tail = node

    def print_structure(self, node=None, level=0, prefix="\nRoot-- "):
        if node is None:
            node = self.root
        print("  " * level + prefix + str(node.data))
        if node.left:
            self.print_structure(node.left, level + 1, "L--- ")
        if node.right:
            self.print_structure(node.right, level + 1, "R--- ")


root = Node(1)
tree = BinaryTree(root)

for i in range(2, 16):
    tree.insert(Node(i))

tree.print_structure()
