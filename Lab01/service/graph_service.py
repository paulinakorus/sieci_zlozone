import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Graph:
    def __init__(self, nodes: int = None, probability: float = None, edges_per_node: int = None, G: nx.Graph = None):
        if G is None:
            if edges_per_node is None:
                self.G = nx.erdos_renyi_graph(n=nodes, p=probability)
            else:
                self.G = nx.barabasi_albert_graph(n=nodes, m=edges_per_node)
        else:
            self.G = G

    def _get_simple_graph(self):
        if isinstance(self.G, nx.MultiGraph):
            return nx.Graph(self.G)
        return self.G

    def plot_graph(self, if_pagerank: bool = False):
        simple_graph = self._get_simple_graph()
        plt.figure(figsize=(12, 8))
        pos = nx.kamada_kawai_layout(simple_graph)
        nodes_size = []
        if if_pagerank:
            pagerank = nx.pagerank(simple_graph)
            nodes_size = [pagerank[node] * 40000 for node in simple_graph.nodes()]
        nx.draw_networkx(
            simple_graph,
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
        simple_graph = self._get_simple_graph()
        nodes = simple_graph.nodes()
        nodes_num = len(nodes)
        edges = simple_graph.edges()
        edges_num = len(edges)

        # print("Nodes:", nodes)
        print(f"Nodes number: {nodes_num}")
        # print("Edges:", edges)
        print(f"Edges number: {edges_num}")

    def plot_degree(self):
        simple_graph = self._get_simple_graph()
        degree_values = [deg for _, deg in simple_graph.degree()]

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

    def plot_betweenness_centrality(self):
        simple_graph = self._get_simple_graph()
        betweeness_value = [bet for _, bet in simple_graph.betweenness_centrality()]
        plt.figure(figsize=(10, 6))
        sns.histplot(
            betweeness_value,
            bins=25,
            kde=True,
            color="steelblue",
            edgecolor="white",
            linewidth=0.5
        )
        plt.title("Betweenness Centrality Distribution", fontsize=14)
        plt.xlabel("Betweenness")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def plot_closeness_centrality(self):
        simple_graph = self._get_simple_graph()
        closeness_value = [clos for _, clos in simple_graph.betweenness_centrality()]
        plt.figure(figsize=(10, 6))
        sns.histplot(
            closeness_value,
            bins=25,
            kde=True,
            color="steelblue",
            edgecolor="white",
            linewidth=0.5
        )
        plt.title("Closeness Centrality Distribution", fontsize=14)
        plt.xlabel("Closeness")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def betweenness_centrality(self):
        return nx.betweenness_centrality(self._get_simple_graph(), normalized=False, endpoints=False) # true czy false

    def max_betweenness_centrality(self):
        betweeness = self.betweenness_centrality()
        return max(betweeness, key=betweeness.get)

    def closeness_centrality(self):
        return nx.closeness_centrality(self._get_simple_graph())

    def clustering_coefficient(self):
        return nx.clustering(self._get_simple_graph())

    def pagerank(self):
        return nx.pagerank(self._get_simple_graph())

    def shortest_path_length(self):
        return nx.shortest_path_length(self._get_simple_graph())

    def diameter(self):
        return nx.diameter(self._get_simple_graph())

    def connected_components(self):
        return nx.number_connected_components(self._get_simple_graph())

    def density(self):
        return nx.density(self._get_simple_graph())

    def get_dataframe(self) -> pd.DataFrame:
        simple_graph = self._get_simple_graph()
        betweeness = self.betweenness_centrality()
        closeness = self.closeness_centrality()
        clustering = self.clustering_coefficient()
        pagerank = self.pagerank()

        largest_cc = max(nx.connected_components(simple_graph), key=len)
        G_largest = simple_graph.subgraph(largest_cc)

        avg_shortest_path = nx.average_shortest_path_length(G_largest)
        diameter = nx.diameter(G_largest)
        num_components = nx.number_connected_components(simple_graph)

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

    def remove_duplicate_edges(self):
        self.G.remove_edges_from(nx.selfloop_edges(self.G))

        if isinstance(self.G, nx.MultiGraph):
            set_list = [set(a) for a in self.G.edges()]
            remove_list = []

            for i in range(len(set_list)):
                edge = set_list.pop(0)
                if set_list.count(edge) > 0:
                    u, v = edge
                    remove_list.append((v, u))

            self.G.remove_edges_from(remove_list)
            self.G = nx.Graph(self.G)


