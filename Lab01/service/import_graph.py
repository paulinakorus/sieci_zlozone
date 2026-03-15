import networkx as nx
import pandas as pd
from networkx import DiGraph

from service.graph_service import MyGraph


class ImportGraph:
    @staticmethod
    def get_radoslaw_from_file(directed: bool = False) -> MyGraph:
        input_file = 'out.radoslaw_email_email'
        df = pd.read_csv(
            input_file,
            sep=r"\s+",
            skiprows=2,
            usecols=[0, 1],
            names=['sender', 'receiver'],
            header=None
        )
        if directed:
            edge_counts = df.groupby(['sender', 'receiver']).size().reset_index(name='edge_count')
            total_counts = df.groupby(['sender']).size().reset_index(name='total_count')
            edge_weights = edge_counts.merge(total_counts, on=['sender'])
            edge_weights['weight'] = edge_weights['edge_count'] / edge_weights['total_count']
            G = DiGraph()

            for _, row in edge_weights.iterrows():
                G.add_edge(row['sender'], row['receiver'], weight=row['weight'])
        else:
            edges = df.values
            G = nx.MultiGraph()
            G.add_edges_from(edges)
        return MyGraph(G=G)