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
    frontier = []
    frontier.append(source)
    expanded = 0

    while frontier:
        current = frontier.pop()
        if current in explored:
            continue

        if graph.nodes[current]["article"] == target:
            path.append(current)
            explored.append(current)
            return path, expanded
        
        explored.append(current)
        path.append(current)

        expanded+=1
        for neighbor in list(graph.adj[current]):
            if neighbor not in explored:
                frontier.append(neighbor)
    return [], expanded

# iterative deepening depth first search
def iddf(graph, source, target):
    visited = []
    parent = {}
    depth = 0

    visited.append(source)

    while True:
        result = dls(graph, source, target, depth, parent, visited, 0)
        found = result[0]
        remaining = result[1]
        expanded = result[2]
        if found:
            return backtrace(parent, source, target, expanded)
        elif not remaining:
            return None
        depth += 1

# recursive depth-limited depth first search
def dls(graph, source, target, depth, parent, visited, expanded):
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
            result = dls(graph, neighbor, target, depth-1, parent, visited, expanded)
            found = result[0]
            remaining = result[1]
            if found:
                return (found, True, expanded)
            if remaining:
                any_remaining = True
        return (None, any_remaining, expanded)
  
def bidirectional_backtrace(intersecting_node, start_parent, end_parent, source, target, expanded):
    path = []
    path.append(intersecting_node)
    ptr = intersecting_node

    while ptr != source: # work way from intersection upwards
        path.append(start_parent[ptr])
        ptr = start_parent[ptr]

    path = path[::-1]
    ptr = intersecting_node

    while ptr != target:
        path.append(end_parent[ptr])
        ptr = end_parent[ptr]

    return path, expanded

def bidirectional_bfs(graph, source, target):
    start_queue = []
    start_visited = []
    start_parent = {}

    end_queue = []
    end_visited = []
    end_parent = {}

    expanded = 0
    start_queue.append(source)
    start_visited.append(source)

    end_queue.append(target)
    end_visited.append(target)

    while start_queue and end_queue:
        vertex1 = start_queue.pop(0)
        vertex2 = end_queue.pop(0)

        if graph.nodes[vertex1]["article"] == target or vertex1 in end_queue:
            return bidirectional_backtrace(vertex1, start_parent, end_parent, source, target, expanded)

        expanded += 1
        for neighbor in list(graph.adj[vertex1]):
            if neighbor not in start_visited:
                start_parent[neighbor] = vertex1
                start_visited.append(neighbor)
                start_queue.append(neighbor)
        
        if graph.nodes[vertex2]["article"] == source or vertex2 in start_queue:
            return bidirectional_backtrace(vertex2, start_parent, end_parent, source, target, expanded)

        for parent in list(graph.pred[vertex2]):
            if parent not in end_visited:
                end_parent[parent] = vertex2
                end_visited.append(parent)
                end_queue.append(parent)
        
    return False
