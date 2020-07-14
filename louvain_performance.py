import community as community_louvain
from collections import Counter
import networkx as nx
import numpy as np
import pandas as pd


def elist_to_graph(df):
    """Converts MASH edgelist to graph object"""
    df.columns = ['sequence1', 'sequence2', 'mashdist', 'pvalue', 'hashmatch']
    G = nx.from_pandas_edgelist(df, 'sequence1', 'sequence2', edge_attr='mashdist')
    return G


def louvain_benchmark(G, points):
    """For each threshold, calculates the number of communities and the community coverage"""
    output = pd.DataFrame(columns=['trial', 'threshold', 'num_comm', 'perc_in_comm'])
    for n in range(0, 50):
        for i in reversed(points):
            G.remove_edges_from([(u, v, d) for (u, v, d) in G.edges(data=True) if d['mashdist'] > i])
            partition = community_louvain.best_partition(G, weight='mashdist')
            members = [v for v in partition.values()]  # list of community members
            counts = Counter(members)
            del counts[0]  # drop unassigned nodes
            comm_size = [counts[i] for i in counts if counts[i] >= 10]
            m = len(comm_size)  # number of communities larger than 3 nodes
            p = 100 * (sum(comm_size) / len(members))  # percentage in communities
            output = output.append(pd.DataFrame([[n, i, m, p]], columns=output.columns))
        G = nx.from_pandas_edgelist(df, 'sequence1', 'sequence2', edge_attr='mashdist')
    return output


data = pd.read_csv('/path/to/edgelist.csv', sep='\t') # import MASH edgelist output
graph = elist_to_graph(data)

p = [round(i, 3) for i in np.linspace(0.025, 0.6, 24)]
louvain_benchmark(graph, p).to_csv('/path/to/output.csv') # output df
