import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

class Graph:
    def __init__(self, random: bool, nodes: int, probability: float = None, edges_per_node: int = None):
        if random:
            self.G = nx.erdos_renyi_graph(n=nodes, p=probability)
        else:
            self.G = nx.barabasi_albert_graph(n=nodes, m=edges_per_node)

    def plot_graph(self):
        plt.figure(figsize=(12, 8))
        pos = nx.kamada_kawai_layout(self.G)
        nx.draw(self.G, pos=pos, with_labels=True, node_color="lightblue", node_size=300)
        plt.title("Erdős–Rényi Random Graph")
        plt.show()

    def print_info(self):
        nodes = self.G.nodes()
        nodes_num = len(nodes)
        edges = self.G.edges()
        edges_num = len(edges)

        print("Nodes:", nodes)
        print(f"Nodes number: {nodes_num}")
        print("Edges:", edges)
        print(f"Edges number: {edges_num}")

    def plot_degree(self):
        degree_values = [deg for _, deg in self.G.degree()]

        plt.figure(figsize=(10, 6))
        sns.histplot(
            degree_values,
            bins=25,
            kde=True,
            color="steelblue",
            edgecolor="white",
            linewidth=0.5
        )
        plt.title("Degree Distribution", fontsize=14)
        plt.xlabel("Degree")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def betweenness_centrality(self):
        return nx.betweenness_centrality(self.G, normalized=False, endpoints=False) # true czy false