import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Entry, Label

class PatriciaTree:
    def __init__(self):
        self.tree = {}

    def insert(self, key):
        current_node = self.tree
        while True:
            for prefix, child in current_node.items():
                common_prefix = self._get_common_prefix(key, prefix)
                if common_prefix:
                    if common_prefix == prefix:
                        current_node = child
                        key = key[len(prefix):]
                        break
                    else:
                        remaining_prefix = prefix[len(common_prefix):]
                        current_node[common_prefix] = {remaining_prefix: child}
                        del current_node[prefix]
                        current_node = current_node[common_prefix]
                        key = key[len(common_prefix):]
                        break
            else:
                current_node[key] = {}
                break

    def _get_common_prefix(self, str1, str2):
        i = 0
        while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
            i += 1
        return str1[:i]

    def visualize(self):
        graph = nx.DiGraph()

        def add_edges(node, parent_label):
            for label, child in node.items():
                graph.add_edge(parent_label, parent_label + label)
                add_edges(child, parent_label + label)

        add_edges(self.tree, "")
        pos = nx.spring_layout(graph)
        plt.figure(figsize=(8, 6))
        nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=700, font_size=10)
        plt.title("Visualización del Patricia Tree")
        plt.show()

# Interfaz Gráfica
def main():
    ptree = PatriciaTree()

    def add_key():
        key = entry_key.get()
        if key:
            ptree.insert(key)
            label_status.config(text=f"Clave '{key}' añadida.")
            ptree.visualize()
        else:
            label_status.config(text="Por favor, introduce una clave.")

    root = Tk()
    root.title("Patricia Tree Visualizer")

    Label(root, text="Clave:").grid(row=0, column=0)
    entry_key = Entry(root)
    entry_key.grid(row=0, column=1)

    Button(root, text="Añadir Clave", command=add_key).grid(row=1, column=0, columnspan=2)
    label_status = Label(root, text="")
    label_status.grid(row=2, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()
