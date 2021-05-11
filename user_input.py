# Data Source: https://snap.stanford.edu/data/wikispeedia.html

# Other sources used:
# https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python#reading-files-importing-data
# https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
# http://planning.cs.uiuc.edu/node50.html
# https://www.cs.cmu.edu/afs/cs/academic/class/15381-s07/www/slides/011807uninformed.pdf
# https://en.wikipedia.org/wiki/Bidirectional_search
# http://www.cs.cmu.edu/afs/andrew/course/15/381-f08/www/lectures/HandoutUninformedSearch.pdf

# Libraries used:
# https://networkx.org/documentation/stable/tutorial.html

import csv
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.
import datetime
import sys
from algorithms import bfs, dfs, iddf, bidirectional_bfs
import psutil
import os

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

def memory_usage_ps():
    process = psutil.Process(os.getpid())
    mem = process.memory_info()
    return mem.rss

# divide the article names into groups of 10 for viewing purposes
def list_of_articles():
    l = []
    total = []
    count = 0
    for name in node_names:
        if count <= 20:
            l.append(name)
            count+=1
        else:
            total.append(l)
            l = []
            count = 0
    return total

def present_articles(article_names,i):
    print(*article_names[i], sep='\n')
    print('\nEnter a number out of %d if you would like to see other pages.' %len(article_names))
    print('Enter \'c\' when you are ready to input.')
    return input('>>').lower()

def perform_algo():
    src = input('Enter the name of your source article: ')
    while src not in node_names:
        src = input('The article name does not exist. Please try again: ')
    target = input('Enter the name of your target article: ')
    while target not in node_names:
        target = input('The article name does not exist. Please try again:')
    
    print('\nPlease choose one of the following for Algorithms: ')
    print('\t\'bfs\' for Breadth First Search')
    print('\t\'bibfs\' for BiDirectional Breadth First Search')
    print('\t\'dfs\' for Depth First Search (note that it does not guarantee the shortest path)')
    print('\t\'iddf\' for Iterative Deepening Depth First Search')
    
    user_input = input('>>').lower()
    start = datetime.datetime.now()
    mem_before = memory_usage_ps()
    if user_input=='bfs':
        result, expanded = bfs(G, src, target)
        print('Path: ' + ' -> '.join(result))
    elif user_input == 'dfs':
        result, expanded = dfs(G, src, target,[], [])
        print('Path: ' + ' -> '.join(result))
    elif user_input == 'iddf':
        result, expanded = iddf(G, src, target)
        print('Path: ' + ' -> '.join(result))
    elif user_input == 'bibfs':
        result, expanded = bidirectional_bfs(G, src, target)
        print('Path: ' + ' -> '.join(result))
    else:
        return
    
    end = datetime.datetime.now()
    mem_after = memory_usage_ps()
    time = (end - start).total_seconds()*1000
    print('Time (ms): ' + str(time))
    print('Nodes Expanded: ' + str(expanded))
    print('Memory Usage: %d bytes' %(mem_after - mem_before))


if __name__ == "__main__":
    article_names = list_of_articles()
    print('Welcome!')
    print('Enter: ')
    print('\t\'a\' if you would like to see a list of articles to choose from.')
    print('\t\'c\' if you would like to enter the article name on your own.')
    print('\tanything else if you would like to end this session.')
    while True:
        user_input = input('>>').lower()
        if user_input =='a':
            user_input = present_articles(article_names,0)
            while True:
                try:
                    num = int(user_input)
                    user_input = present_articles(article_names, num-1)
                except ValueError:
                    if user_input=='c':
                        perform_algo()
                        break
                    else:
                        sys.exit(0)
        elif user_input == 'c':
            perform_algo()
        else:
            sys.exit(0)

        print('\nEnter: ')
        print('\t\'a\' if you would like to see a list of articles to choose from.')
        print('\t\'c\' if you would like to enter the article name on your own.')
        print('\tanything else if you would like to end this session.')
        
        
    
