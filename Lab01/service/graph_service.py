import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from fontTools.misc.cython import returns


class Graph:
    def __init__(self, nodes: int, probability: float = None, edges_per_node: int = None):
        if edges_per_node is None:
            self.G = nx.erdos_renyi_graph(n=nodes, p=probability)
        else:
            self.G = nx.barabasi_albert_graph(n=nodes, m=edges_per_node)

    def plot_graph(self, if_pagerank: bool = False):
        plt.figure(figsize=(12, 8))
        pos = nx.kamada_kawai_layout(self.G)
        nodes_size = []
        if if_pagerank:
            pagerank = nx.pagerank(self.G)
            nodes_size = [pagerank[node] * 40000 for node in self.G.nodes()]
        nx.draw_networkx(
            self.G,
            pos=pos,
            with_labels=True,
            node_color="lightblue",
            node_size=nodes_size if if_pagerank else 30,
            edge_color="gray",
            alpha=0.7
        )
        plt.tight_layout()
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

    def max_betweenness_centrality(self):
        betweeness = self.betweenness_centrality()
        return max(betweeness, key=betweeness.get)

    def closeness_centrality(self):
        return nx.closeness_centrality(self.G)

    def clustering_coefficient(self):
        return nx.clustering(self.G)

    def pagerank(self):
        return nx.pagerank(self.G)

    def shortest_path_length(self):
        return nx.shortest_path_length(self.G)

    def diameter(self):
        return nx.diameter(self.G)

    def connected_components(self):
        return nx.number_connected_components(self.G)

    def density(self):
        return nx.density(self.G)

    def get_dataframe(self) -> pd.DataFrame:
        betweeness = self.betweenness_centrality()
        closeness = self.closeness_centrality()
        clustering = self.clustering_coefficient()
        pagerank = self.pagerank()

        largest_cc = max(nx.connected_components(self.G), key=len)
        G_largest = self.G.subgraph(largest_cc)

        avg_shortest_path = nx.average_shortest_path_length(G_largest)
        diameter = nx.diameter(G_largest)
        num_components = nx.number_connected_components(self.G)

        df = pd.DataFrame({
            "betweenness": pd.Series(betweeness),
            "closeness": pd.Series(closeness),
            "clustering": pd.Series(clustering),
            "pagerank": pd.Series(pagerank),
            "avg_shortest_path": avg_shortest_path,
            "diameter": diameter,
            "num_components": num_components,
        })
        return df



