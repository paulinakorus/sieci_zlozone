import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import kendalltau


class MyGraph:
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

    def print_info(self, text: bool = True):
        simple_graph = self._get_simple_graph()
        nodes = simple_graph.nodes()
        nodes_num = len(nodes)
        edges = simple_graph.edges()
        edges_num = len(edges)

        print("Nodes:", nodes) if text else None
        print(f"Nodes number: {nodes_num}")
        print("Edges:", edges) if text else None
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
        betweenness = nx.betweenness_centrality(simple_graph)
        betweenness_values = list(betweenness.values())
        plt.figure(figsize=(10, 6))
        sns.histplot(betweenness_values, bins=25, kde=True, color="steelblue", edgecolor="white", linewidth=0.5)
        plt.title("Betweenness Centrality Distribution", fontsize=14)
        plt.xlabel("Betweenness")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def plot_closeness_centrality(self):
        simple_graph = self._get_simple_graph()
        closeness = nx.closeness_centrality(simple_graph)
        closeness_values = list(closeness.values())
        plt.figure(figsize=(10, 6))
        sns.histplot(closeness_values, bins=25, kde=True, color="steelblue", edgecolor="white", linewidth=0.5)
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

    def connected_components(self):
        return nx.number_connected_components(self._get_simple_graph())

    def density(self):
        return nx.density(self._get_simple_graph())

    def nodes_without_edges(self):
        nodes_num = len([node for node,degree in dict(self.G.degree()).items() if degree == 0])
        print(f"Nodes without edges: {nodes_num}")

    def get_dataframe(self) -> pd.DataFrame:
        simple_graph = self._get_simple_graph()
        betweeness = self.betweenness_centrality()
        closeness = self.closeness_centrality()
        clustering = self.clustering_coefficient()
        pagerank = self.pagerank()

        diameter, avg_shortest_path = self.diameter_and_shortest_path_length()
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

    def kendall(self):
        simple_graph = self._get_simple_graph()

        degree = list(dict(nx.degree(simple_graph)).values())
        betweeness = list(nx.betweenness_centrality(simple_graph).values())
        closeness = list(nx.closeness_centrality(simple_graph).values())

        ken_deg_bet, _ = kendalltau(degree, betweeness)
        ken_deg_close, _ = kendalltau(degree, closeness)
        ken_bet_close, _ = kendalltau(betweeness, closeness)

        print("Korelacja Kendall τ:")
        print("degree vs betweenness:", ken_deg_bet)
        print("degree vs closeness:", ken_deg_close)
        print("betweenness vs closeness:", ken_bet_close)

    def top_nodes(self):
        simple_graph = self._get_simple_graph()
        n = 5

        degree = dict(nx.degree(simple_graph))
        betweeness = nx.betweenness_centrality(simple_graph)
        closeness = nx.closeness_centrality(simple_graph)

        print("Top degree:")
        print(sorted(degree, key=degree.get, reverse=True)[:n])
        print("Top betweenness:")
        print(sorted(betweeness, key=betweeness.get, reverse=True)[:n])
        print("Top closeness:")
        print(sorted(closeness, key=closeness.get, reverse=True)[:n])

    def diameter_and_shortest_path_length(self):
        simple_graph = self._get_simple_graph()
        largest_cc = max(nx.connected_components(simple_graph), key=len)
        G_largest = simple_graph.subgraph(largest_cc)

        avg_shortest_path = nx.average_shortest_path_length(G_largest)
        diameter = nx.diameter(G_largest)
        return diameter, avg_shortest_path

    def if_strongly_connected(self):
        if self.G.is_directed():
            return nx.is_strongly_connected(self.G)
        return None