# Data Source: https://snap.stanford.edu/data/wikispeedia.html
# Other sources used:
# https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python#reading-files-importing-data
# Libraries used:
# https://networkx.org/documentation/stable/tutorial.html

import csv
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.

node_path = "./wikispeedia_paths-and-graph/articles.tsv"
edge_path = "./wikispeedia_paths-and-graph/links.tsv"

with open(node_path, 'r') as tsv_file: # Open the file
    nodereader = csv.reader(tsv_file, delimiter="\t") # Read the csv
    # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
    nodes = [n for n in nodereader][12:]

node_names = [n[0] for n in nodes] # Get a list of only the node names

with open(edge_path, 'r') as edgetsv: # Open the file
    edgereader = csv.reader(edgetsv, delimiter="\t") # Read the csv
    edges = [tuple(e) for e in edgereader][12:] # Retrieve the data

# print(len(node_names))
# print(len(edges))
# print(node_names[0])
# print(edges[0])

G = nx.Graph()
G.add_nodes_from(node_names)
G.add_edges_from(edges)

print(nx.info(G))

# print(list(G.adj["Orca"]))
print(list(G.neighbors("Orca")))