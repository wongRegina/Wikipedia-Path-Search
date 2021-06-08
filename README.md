# Wikipedia Path Search

The goal of this application is to find one of the shortest
paths to get from one Wikipedia page to another Wikipedia page.
The edges are is determined by hyperlinks on the page. The application will return 
one of the shortest paths using the specified algorithm.

## Requirements

### Python
This program requires Python version 3.7, which can be obtained from http://www.python.org. 
To check the Python version installed on your system, type:

    python --version 
        
The following Python Libraries were used:
import

    import networkx as nx
    import psutil
    
The following install statements were used:
    
    pip install networkx
    pip install psutil
    
## Running the program
Once you have the file on your computer, go to the terminal (command prompt). 
Change the directory to the folder where 'user_input.py' is located.
Once the terminal is in that folder, you can call:
    
       python user_input.py
    
_Note: python is set as the environmental variable. If it isn't set, use the path to python.exe_

After follow the instructions on the terminal.

    'a' if you would like to see a list of articles to choose from.
    'c' if you would like to enter the article name on your own.
    
Inputting 'a' would give you the first 20 articles on Wikipedia in alphabetical order. You can enter in a number to go to different pages

Inputting 'c' would prompt you to enter a source article.
    
    Enter the name of your source article:
    
Once you enter a valid article, it would prompt you to enter a target article.

    Enter the name of your target article:

Once a valid article is enter it would ask for the algorithm to run

    'bfs' for Breadth First Search
    'bibfs' for Bidirectional Breadth First Search
    'dfs' for Depth First Search (note that it does not guarantee the shortest path)
    'iddf' for Iterative Deepening Depth First Search

Once you choose an algorithm, it would run the code and output the following information

    Path:
    Time (ms):
    Nodes Expanded:
    Memory Usage:
    