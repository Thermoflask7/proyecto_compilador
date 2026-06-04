class Node:
    def __init__(self, category, value, parent, line):
        self.children = []
        self.category = category
        self.value = value
        self.line = line
    
    def add_child(self, category, value, line):
        self.children.append(Node(self.category, self.value, self.line))

    def print_tree(self):
        pass
