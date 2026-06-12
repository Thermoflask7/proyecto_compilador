class Node:
    def __init__(self, category, value=None, line=None):
        self.category = category
        self.value = value
        self.line = line
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def print_tree(self, level=0):
        if self.value is not None:
            print("  " * level + f"{self.category}: {self.value}")
        else:
            print("  " * level + f"{self.category}")
        for child in self.children:
            child.print_tree(level + 1)