import community as community_louvain
import networkx as nx
import numpy as np
import pandas as pd
import random
import sklearn.metrics as metric


def elist_to_graph_threshold(df, t):
    """Converts MASH edgelist to graph object at threshold t"""
    df.columns = ['sequence1', 'sequence2', 'mashdist', 'pvalue', 'hashmatch']
    G = nx.from_pandas_edgelist(df, 'sequence1', 'sequence2', edge_attr='mashdist')
    G.remove_edges_from([(u, v, d) for (u, v, d) in G.edges(data=True) if d['mashdist'] > t])
    return G


def louvain_labels(G):
    """Runs Louvain algorithm on the graph"""
    partition = community_louvain.best_partition(G, weight='mashdist')  # run louvain
    partition = pd.DataFrame.from_dict(partition, orient='index')  # convert communities to df
    partition.index.name = 'sequence'  # rename index
    return partition


def cleanup(communities, labels, min_size):
    """Creates a single df with communities (of min_size) and metadata labels"""
    communities = communities.rename({0: 'community'}, axis='columns')  # rename column
    output = pd.merge(communities, labels, on='sequence')  # merge with node labels df
    output = output[output['community'] != 0]  # drop nodes without community
    counts = output['community'].value_counts()  # community sizes
    output = output[~output['community'].isin(counts[counts < min_size].index)]  # communities with min_size members
    return output


def perm_test(df, n, hom):
    """Runs a permutation test of size n against homogeneity score hom"""
    perm_test_values = []
    comm = list(df['community'])
    for i in range(0, n):
        random_comm = random.sample(comm, len(comm))
        perm_test_values.append(metric.homogeneity_score(df['label'].to_numpy(),
                                                         np.asarray(random_comm)))
    p_val = len(np.where(perm_test_values >= hom)[0]) / n
    return p_val


data = pd.read_csv('/path/to/edgelist.csv', sep='\t')
graph = elist_to_graph_threshold(data, 0.05)

metadata_labels = pd.read_csv('/path/to/labels.csv')  # import metadata labels

part = louvain_labels(graph)

combined_df = cleanup(part, metadata_labels, 10)

# calculate homogeneity and completeness for metadata combination 'label'
score_hom = metric.homogeneity_score(combined_df['label'].to_numpy(),
                                     combined_df['community'].to_numpy())

score_com = metric.completeness_score(combined_df['label'].to_numpy(),
                                      combined_df['community'].to_numpy())

print(perm_test(combined_df, 1000, score_hom))
