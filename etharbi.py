class NoShortestPathError(Exception):
    pass

class NegativeCycleError(NoShortestPathError):
    def __init__(self, weight, cycle):
        self.weight = weight
        self.cycle = cycle

    def __str__(self):
        return f"Weight {self.weight}: {self.cycle}"

#  Nodes
example_graph = {
     "Node1": {
        "Node2": 1,
        "Node3": 2,
        "Node4": 3,
        "Node5": 3,
        "Node6": 5,
    },
     "Node2": {
        "Node1": 3,
        "Node3": 0,
        "Node4": 3,
        "Node5": 8,
        "Node6": 2,
    },
     "Node3": {
        "Node1": 3,
        "Node2": 0,
        "Node4": 3,
        "Node5": 0,
        "Node6": 0,
    },
     "Node4": {
        "Node1": 3,
        "Node2": 3,
        "Node3": 4,
        "Node5": 8,
        "Node6": 6,
    },
     "Node5": {
        "Node1": 0,
        "Node2": 3,
        "Node3": 2,
        "Node4": 3,
        "Node6": 4,
    },
    "Node6": {
        "Node1": 3,
        "Node2": 7,
        "Node3": 3,
        "Node4": 3,
        "Node5": 4,
    },
}



def all_vertices(graph):
    """Return a set of all vertices in a graph.
    
    graph -- a weighted, directed graph.
    """
    vertices = set()
    for v in graph.keys():
        vertices.add(v)
        for u in graph[v].keys():
            vertices.add(u)
    return vertices

def shortest_path_bellman_ford(*, graph, start, end):
    """Finds the least cost path from start to end in graph,
    using the Bellman-Ford algorithm.
    
    If a negative cycle exists, raise NegativeCycleError.
    If no shortest path exists, raise NoShortestPathError.
    """
    n = len(all_vertices(graph))

    dist = {}
    pred = {}

    def is_dist_infinite(v):
        return v not in dist

    def walk_pred(start, end):
        path = [start]
        v = start
        while v != end:
            v = pred[v]
            path.append(v)
        path.reverse()
        return path

    def find_cycle(start):
        nodes = []
        node = start
        while True:
            if node in nodes:
                cycle = [
                    node,
                    *reversed(nodes[nodes.index(node) :]),
                ]
                print(nodes)
                print(cycle)
                return cycle
            nodes.append(node)
            if node not in pred:
                break
            node = pred[node]

    dist[start] = 0

    # Relax approximations (n-1) times.

    for _ in range(n - 1):
        for tail in graph.keys():
            if is_dist_infinite(tail):
                continue
            for head, weight in graph[tail].items():
                alt = dist[tail] + weight
                if is_dist_infinite(head) or (
                    alt < dist[head]
                ):
                    dist[head] = alt
                    pred[head] = tail

    # Check for negative cycles.

    for tail in graph.keys():
        for head, weight in graph[tail].items():
            if (dist[tail] + weight) < dist[head]:
                cycle = find_cycle(tail)
                cycle_weight = sum(
                    graph[c_tail][c_head]
                    for (c_tail, c_head) in zip(cycle, cycle[1:])
                        
                )
                           
                raise NegativeCycleError(
                    cycle_weight, cycle
                )
             

    # Build shortest path.

    if is_dist_infinite(end):
        raise NoShortestPathError

    best_weight = dist[end]
    best_path = walk_pred(end, start)
    
    for (head, tail) in zip(best_path, best_path[1:]):
            gas_price = graph[head][tail]
            
            print(f" {head} --> ( {gas_price} wei ) --> {tail} ")
    return best_weight, best_path


# shortest_path_bellman_ford(
#     graph=example_graph, start="Node1", end="Node5"
# )

print( shortest_path_bellman_ford(
    graph=example_graph, start="Node1", end="Node5"
) )

# time complexity 0 (|v| * |e|)

