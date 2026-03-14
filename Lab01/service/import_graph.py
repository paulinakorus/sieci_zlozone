import networkx as nx
import pandas as pd

from service.graph_service import Graph


class ImportGraph:
    @staticmethod
    def get_radoslaw_from_file() -> Graph:
        input_file = 'out.radoslaw_email_email'
        df = pd.read_csv(input_file, sep=r"\s+", skiprows=2, header=None)
        edges = df.iloc[:, :2].values
        G = nx.MultiGraph()
        G.add_edges_from(edges)
        return Graph(G=G)