from copy import copy,deepcopy

class Item:
    def __init__(self,w,v):
        self.w = w
        self.v = v
        self.r = v/w
    def __lt__(self,other):
        return self.r < other.r

class Node:
    def __init__(self):
        self.layer 		= -1
        self.info 		= []
        self.optimum_v 	= -1
        self.total_w 	= 0
    def __lt__(self,other):
        return self.optimum_v < other.optimum_v


class Knapsack:
    def __init__(self,N,maxw):
        self.N 			= N
        self.max_w = maxw
        self.max_v 	= 0
        self.items 		= []
        self.quene 		= []
    def add_item(self,item):
        self.items.append(item)
    def sort_item(self):
        self.items.sort(reverse=True)
    def calculate_matrix_v(self,node):
        w = 0
        v = 0
        for i in node.info:
            w += i.w
            v += i.v
        if w > self.max_w:
            node.optimum_v = -1
            return
        node.total_w = w
        for j in range(node.layer + 1, self.N):
            if w + self.items[j].w <= self.max_w:
                w += self.items[j].w
                v += self.items[j].v
            else:
                v += self.items[j].r*(self.max_w-w)
                break
        node.optimum_v = v
		
    def solve(self):
        node = Node()
        self.calculate_matrix_v(node)
        self.max_v = node.optimum_v
        self.quene.append(node)
        flag = 0
        while self.quene:
            if flag == 0:
                node = self.quene.pop()
            flag = 1
			
            node_L = deepcopy(node)
            node_L.layer += 1
            node_L.info.append(self.items[node_L.layer])
			
            self.calculate_matrix_v(node_L)
            if node_L.optimum_v > 0 and node_L.optimum_v <= self.max_v:
                self.quene.append(node_L)
            
            node_R = deepcopy(node)
            node_R.layer += 1
			
            self.calculate_matrix_v(node_R)
            if node_R.optimum_v > 0 and node_R.optimum_v <= self.max_v:
                self.quene.append(node_R)
				
            self.quene.sort()
            node = self.quene.pop()
            
            if node.layer == 3:
                break
				
        return node

def main():
    print("W List:")
    w = [int(n) for n in input().split()]
    print("V List:")
    v = [int(n) for n in input().split()]
    print("C:")
    C = int(input())
    k = Knapsack(len(w),C)
    [k.add_item(Item(w[i],v[i])) for i in range(len(w))]
    k.sort_item()
    nn = k.solve()
    print("Total V: ",nn.optimum_v)
    print("Total W: ",nn.total_w)
    print("Method: ", end = " ");[print((i.w,i.v), end = " ") for i in nn.info]

if __name__ == "__main__":
    main()
