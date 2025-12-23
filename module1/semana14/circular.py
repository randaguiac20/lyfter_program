"""
Extra exercise - Circular data structure
"""

class Node:
    """Defines a single node in the stack."""
    def __init__(self, data):
        self.data = data
        self.next = None

class Circular:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, node):
        if self.head is None:
            # First node points to itself
            self.head = self.tail = node
            node.next = node
        else:
            node.next = self.head
            self.tail.next = node
            self.head = node

    def pop(self):
        if self.head is None:
            return None

        if self.head == self.tail:
            # Only one node
            data = self.head.data
            self.head = self.tail = None
            return data

        data = self.head.data
        self.head = self.head.next
        self.tail.next = self.head  # Important: maintain circular reference
        return data

    def print_structure(self, action, nodes=None, last=None, first=None):
        action = "Pushing nodes" if action == "push" else "Popping node"
        print(f"\n{action} in the Circular List:")

        if self.head is None:
            print("No nodes to display.")
            return
        current_node = self.head
        if nodes:
            for _ in range(1, nodes):
                if current_node.data == last and current_node.next.data == first:
                    print(f"Node: {current_node.data} -> ", end="")
                    current_node = current_node.next.next  # Skip the "one"
                if current_node != self.head:
                    print(f"Node: {current_node.data} -> ", end="")
                    current_node = current_node.next
            print("(back to head)")
        else:
            first_pass = True
            while first_pass or current_node != self.head:
                first_pass = False
                print(f"Node: {current_node.data} -> ", end="")
                current_node = current_node.next
            print("(back to head)")

        

if __name__ == "__main__":
    circular = Circular()
    all_nodes = ["one", "two", "three", "four","five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
    "twenty-one", "twenty-two", "twenty-three", "twenty-four", "twenty-five",
    "twenty-six", "twenty-seven", "twenty-eight", "twenty-nine", "thirty",
    "thirty-one", "thirty-two", "thirty-three", "thirty-four", "thirty-five"]
    nodes = ["one", "two", "three", "four","five", "one", "six"]
    # Pushing Nodes
    first = nodes[0]
    last = nodes[-1]
    qnodes = len(nodes) * 2
    for node in nodes:
        circular.push(Node(node))
    circular.print_structure("push", qnodes, last, first)
    print()
    # Popping Nodes
    circular.pop()
    for nodes in range(1, len(nodes)):
        circular.pop()
        circular.print_structure("pop")
    print()
