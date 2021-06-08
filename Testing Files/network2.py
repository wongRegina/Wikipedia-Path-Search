# Data Source: https://snap.stanford.edu/data/wikispeedia.html
# Other sources used:
# https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python#reading-files-importing-data
# Libraries used:
# https://networkx.org/documentation/stable/tutorial.html
# pseudocode:
# https://artint.info/html/ArtInt_63.html#:~:text=Branch%2Dand%2Dbound%20search%20is%20typically%20used%20with%20depth%2D,as%20shorter%20paths%20are%20found

import csv
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.
import queue

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

G = nx.DiGraph()
for n in node_names:
    G.add_node(n, article=n)
G.add_edges_from(edges)

def dfs(graph, source, target, path, explored, expanded):
    frontier = queue.Queue()
    frontier.put(source)

    while frontier:
        current = frontier.get() # pop
        if current in explored:
            continue

        if G.nodes[current]["article"] == target:
            path.append(current)
            explored.append(current)
            print(path)
            return path
        
        explored.append(current)
        path.append(current)

        for neighbor in list(graph.adj[current]):
            expanded.append(current)
            if neighbor not in explored:
                frontier.put(neighbor)
    return [], expanded


# print(nx.info(G))
# print(G.edges)
# print(dfs(G, "Orca", "Kangaroo", [], []))
o = dfs(G, "14th_century", "Fire", [], [])
s = ''.join(o)

output = open("output.txt", 'w')
output.write(s)
""" dfs(G, "Batman", "Jazz", [], [])
dfs(G, "Edgar_Allan_Poe", "Zebra", [], [])
dfs(G, "Achilles_tendon", "Ivory", [], [])
dfs(G, "Planet", "Jimmy_Wales", [], []) """