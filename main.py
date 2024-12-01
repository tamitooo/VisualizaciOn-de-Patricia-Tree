import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Canvas, StringVar


class PatriciaTree:
    def __init__(self):
        self.tree = {}

    def insert(self, key):
        node = self.tree
        for char in key:
            if char not in node:
                node[char] = {}
            node = node[char]
        node["*"] = True

    def search(self, key):
        node = self.tree
        for char in key:
            if char not in node:
                return False
            node = node[char]
        return "*" in node

    def delete(self, key):
        def helper(node, key, depth):
            if depth == len(key):
                if "*" in node:
                    del node["*"]
                    return len(node) == 0
                return False
            char = key[depth]
            if char in node and helper(node[char], key, depth + 1):
                del node[char]
                return len(node) == 0
            return False

        helper(self.tree, key, 0)



class PatriciaTreeApp:
    def __init__(self, root):
        self.tree = PatriciaTree()
        self.root = root
        self.root.title("Patricia Tree Visualizer")
        self.canvas = Canvas(root, width=0, height=0, bg="white")
        self.canvas.pack()
        self.key_var = StringVar()

        Label(root, text="Clave:").pack()
        Entry(root, textvariable=self.key_var).pack()
        Button(root, text="Insertar", command=self.insert_key).pack()
        Button(root, text="Buscar", command=self.search_key).pack()
        Button(root, text="Eliminar", command=self.delete_key).pack()

    def draw_tree(self):
        self.canvas.delete("all")
        G = nx.DiGraph()

        def add_edges(node, parent, prefix=""):
            for char, subtree in node.items():
                if char != "*":
                    G.add_edge(prefix, prefix + char)
                    add_edges(subtree, prefix + char, prefix + char)

        add_edges(self.tree.tree, "")

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, ax=plt.gca(), with_labels=True, node_color="lightblue", node_size=500, font_size=10)
        plt.show()

    def insert_key(self):
        key = self.key_var.get()
        self.tree.insert(key)
        self.draw_tree()

    def search_key(self):
        key = self.key_var.get()
        found = self.tree.search(key)
        Label(self.root, text=f"Clave {'encontrada' if found else 'no encontrada'}").pack()

    def delete_key(self):
        key = self.key_var.get()
        self.tree.delete(key)
        self.draw_tree()


if __name__ == "__main__":
    root = Tk()
    app = PatriciaTreeApp(root)
    root.mainloop()
