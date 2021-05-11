
import queue

def backtrace(parent, start, end, expanded):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path, expanded

# breadth first search
def bfs(graph, source, target):
    queue = []
    visited = []
    parent = {}
    expanded = 0

    queue.append(source)
    visited.append(source)

    while queue:
        vertex = queue.pop(0)

        if graph.nodes[vertex]["article"] == target:
            return backtrace(parent, source, target, expanded)

        expanded += 1
        for neighbor in list(graph.adj[vertex]):
            if neighbor not in visited:
                parent[neighbor] = vertex
                visited.append(neighbor)
                queue.append(neighbor)

# depth first search
def dfs(graph, source, target, explored, path):
    frontier = queue.Queue()
    frontier.put(source)
    expanded = 0

    while frontier:
        current = frontier.get() # pop
        if current in explored:
            continue

        if graph.nodes[current]["article"] == target:
            path.append(current)
            explored.append(current)
            print(path)
            return path, expanded
        
        explored.append(current)
        path.append(current)

        expanded+=1
        for neighbor in list(graph.adj[current]):
            if neighbor not in explored:
                frontier.put(neighbor)
    return [], expanded

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
            return backtrace(parent, source, target, expanded)
        elif not remaining:
            return None
        depth += 1

# recursive depth-limited depth first search
def dls(graph, source, target, depth, parent, visited):
    expanded = 0
    if depth == 0:
        if graph.nodes[source]["article"] == target:
            return (source, True, expanded)
        else:
            return (None, True, expanded)
    elif depth > 0:
        any_remaining = False
        expanded += 1
        for neighbor in list(graph.adj[source]):
            if neighbor not in visited:
                parent[neighbor] = source
                visited.append(neighbor)
            result = dls(graph, neighbor, target, depth-1, parent, visited)
            found = result[0]
            remaining = result[1]
            if found:
                return (found, True, expanded)
            if remaining:
                any_remaining = True
        return (None, any_remaining, expanded)