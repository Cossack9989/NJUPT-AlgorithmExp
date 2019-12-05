import math
from heapq import *

print("Places Summary:")
n = int(input())
G = {}
for i in range(n):
    G[str(i+1)] = {}
while True:
    try:
        print("How long travelling from place A to B will take?")
        record = [int(i) for i in input().split(' ')]
        G[str(record[0])][str(record[1])] = record[2]
        G[str(record[1])][str(record[0])] = record[2]
    except Exception as e:
        break
bestcost = math.inf
nowcost = 0
 
class Node:
    def __init__(self, w=math.inf, route=[], cost=0):
        self.w = w
        self.route = route
        self.cost = cost

    def __lt__(self,other):
        return int(self.w) < int(other.w)
    
    def __str__(self):
        return "Node Weight:"+str(self.w)+" Node Route:"+str(self.route)+" Node Cost:"+str(self.cost)
        
 
def BBTSP(graph, n, s):
    global bestcost, bestroute
    heap = []
    
    start = Node(route=[str(s)])
    
    heap.append(start)
    
    while heap:
        nownode = heappop(heap)
        for e in [r for r in graph if r not in nownode.route]:
            node = Node(w=graph[nownode.route[-1]][e], route=nownode.route+[e], cost=nownode.cost+graph[nownode.route[-1]][e])
            if node.cost >= bestcost:
                continue

            if len(node.route)==4:
                wholecost = graph[node.route[-1]][s]+node.cost
                if wholecost < bestcost:
                    bestcost = wholecost
                    bestroute = node.route
                    print(bestcost,bestroute)
                    
            heap.append(node)

    return (bestcost,bestroute)
        
    
print("Best Cost & Route:",BBTSP(G, n, '1'))