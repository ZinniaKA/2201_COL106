"""program to find the sequence of routers having maximum capacity provided a network of n routers """
path=[] #global variable initiated to [] after each main function call, stores the sequence of node visited in order

def find_sequence(p,v,t):
    """
    finds the sequence from source router to target router in the path having maximum capacity
    INPUT:
    p : list of int-- vertices visited on the maximum capacity path from soure to target
    v : int --current vertex/router
    t : int -- target vertex/router
    OUTPUT:
    path: list of int-- sequence of routers visited
    """
    if (v == "x"):
        return
    find_sequence(p,p[v], t)
    path.append(v)
    if v==t: #target reached
        return path
    
def form_graph(n,links):   
    """
    function to forms adjacency list representation of graph
    INPUT:
    n: int--no.of vertices in graph
    links: tuple of three elements of type int --(u,v,c), where u and v are end pts. of an edge(link) and c is the maximum capacity of the link
    RETURNS :graph--list of list of tuple of 2 elements ---for some i<n graph[i] correspond to i th vertex and is a list of tuples (c,v) where s.t. vertex i and v have a link of capacity c
    """
    graph=[[] for i in range(n)]
    i=0
    m=len(links) #no. of edges
    for i in range (0, m):
        (a,b,weight)=links[i]
        graph[a].append((weight,b))
        graph[b].append((weight,a))
    
    return graph

def findMaxCapacity(n,links,s,t):
    """
    main function
    for a network of n routers connected by links s.tnetwork is connected, we find the  maximum size of packet which can be transferred from source to target and produce the route followed from source to target by that packet

    INPUT:
    n: int-- no. of routers in network
    links: a list of 3-tuples of integers. A tuple (u, v, c) in this list represents a bidirectional link of capacity c between u and v, where u, v ∈ {0, . . . , n - 1}
    s:int-- the source router (s ∈ {0, . . . , n - 1})
    t:int-- the target router (s ∈ {0, . . . , n - 1})

    OUTPUT:
    (C,route)
    C :int-- largest number such that a packet of size C can be transferred over the network from s to t.
    route:list of int -- a list of numbers from the set {0, . . . , n - 1} such that route[0] is s, route[len(route)-1] is t, and for each i, there exists a link of capacity at least C between route[i-1] and route[i]
    """
    global path

    graph = form_graph(n,links)    #form the graph using links
    max_cap = [-float('inf')]*(len(graph))    #to keep track of maximum capacity
    parent = ["x"]*len(graph) # To get the path at the end of the algorithm
    
    current = []     #to keep track of maximum capacity routers obtained thus far via implementing a minimum priority queue
    current.append((0, s))
    max_cap[s] = float('inf')
    current = sorted(current)

    while (len(current)>0):
        temp = current[-1]
        current_s = temp[1]
        del current[-1]
        for vertex in graph[current_s]:#for finding the maximimum capacity link to vertex from current vertex

            distance = max(max_cap[vertex[1]],min(max_cap[current_s], vertex[0]))

            if (distance > max_cap[vertex[1]]):
                
                max_cap[vertex[1]] = distance
                parent[vertex[1]] = current_s
                current.append((distance, vertex[1]))
                current = sorted(current)

    #find the path traversed
    find_sequence(parent, t, t)
    C=max_cap[t]
    route = path
    path = [] #initialise the path to empty list for next function call
    return (C,route)