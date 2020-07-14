import numpy as np
import networkx as nx
import pandas as pd


def elist_to_graph(df):
    """Converts MASH edgelist to graph object"""
    df.columns = ['sequence1', 'sequence2', 'mashdist', 'pvalue', 'hashmatch']
    G = nx.from_pandas_edgelist(df, 'sequence1', 'sequence2', edge_attr='mashdist')
    return G


def lcc(G, points):
    """For each threshold, calculates the size of the largest connected component"""
    lcc = []
    for i in reversed(points):
        G.remove_edges_from([(u, v, d) for (u, v, d) in G.edges(data=True) if d['mashdist'] > i])
        lcc.append(len(max(nx.connected_components(G), key=len)))
        return lcc


def ncc(G, points):
    """For each threshold, calculates the number of connected components"""
    ncc = []
    for i in reversed(points):
        G.remove_edges_from([(u, v, d) for (u, v, d) in G.edges(data=True) if d['mashdist'] > i])
        ncc.append(nx.number_connected_components(G))
        return ncc


data = pd.read_csv('/path/to/edgelist.csv', sep='\t') # import MASH edgelist output
graph = elist_to_graph(data)

p = np.linspace(0, 1, 10000)
largest_cc = lcc(graph, p)
num_cc = ncc(graph, p)

pd.DataFrame({"Threshold": points, "Largest Connected Component": largest_cc[::-1],
                   "Number of Connected Components": num_cc[::-1]}).to_csv('/path/to/output.csv') # output df

