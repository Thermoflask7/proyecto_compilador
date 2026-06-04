class Node:
    def __init__(self, category, value=None, line=None):
        self.category = category
        self.value = value
        self.line = line
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def print_tree(self, level=0):
        print("  " * level + f"{self.category}: {self.value}")
        for child in self.children:
            child.print_tree(level + 1)