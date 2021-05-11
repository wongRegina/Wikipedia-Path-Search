# Data Source: https://snap.stanford.edu/data/wikispeedia.html

# Other sources used:
# https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python#reading-files-importing-data
# https://en.wikipedia.org/wiki/Breadth-first_search
# https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search

# Libraries used:
# https://networkx.org/documentation/stable/tutorial.html

import csv
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.
from memory_profiler import memory_usage, profile

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

print(nx.info(G))
print()

# print(list(G.adj["Orca"]))
# print(G.nodes["Orca"])

def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

# breadth first search
def bfs(graph, source, target):
    queue = []
    visited = []
    parent = {}

    queue.append(source)
    visited.append(source)

    while queue:
        vertex = queue.pop(0)

        if G.nodes[vertex]["article"] == target:
            return backtrace(parent, source, target)

        for neighbor in list(graph.adj[vertex]):
            if neighbor not in visited:
                parent[neighbor] = vertex
                visited.append(neighbor)
                queue.append(neighbor)

print(bfs(G, "Orca", "Kangaroo"))
print(bfs(G, "14th_century", "Fire"))
print(bfs(G, "Batman", "Jazz"))
print(bfs(G, "Edgar_Allan_Poe", "Zebra"))
print(bfs(G, "Achilles_tendon", "Ivory"))
print(bfs(G, "Planet", "Jimmy_Wales"))
print("---")

@profile
# iterative deepening depth first search
def iddf(graph, source, target):
    visited = []
    parent = {}
    depth = 0

    visited.append(source)

    while True:
        result = dls(graph, source, target, depth, parent, visited)
        found = result[0]
        remaining = result[1]
        if found:
            return backtrace(parent, source, target)
        elif not remaining:
            return None
        depth += 1

@profile
# recursive depth-limited depth first search
def dls(graph, source, target, depth, parent, visited):
    if depth == 0:
        if G.nodes[source]["article"] == target:
            return (source, True)
        else:
            return (None, True)
    elif depth > 0:
        any_remaining = False
        for neighbor in list(graph.adj[source]):
            if neighbor not in visited:
                parent[neighbor] = source
                visited.append(neighbor)
            result = dls(graph, neighbor, target, depth-1, parent, visited)
            found = result[0]
            remaining = result[1]
            if found:
                return (found, True)
            if remaining:
                any_remaining = True
        return (None, any_remaining)

print(iddf(G, "Orca", "Kangaroo"))
""" print(iddf(G, "14th_century", "Fire"))
print(iddf(G, "Batman", "Jazz"))
print(iddf(G, "Edgar_Allan_Poe", "Zebra"))
print(iddf(G, "Achilles_tendon", "Ivory"))
print(iddf(G, "Planet", "Jimmy_Wales"))
print("---")    """    

# print(list(G.pred["Kangaroo"]))
