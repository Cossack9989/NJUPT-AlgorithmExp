class tree(object):
    def __init__(self,w,v,left=None,right=None,parent=None,isLeftVisited=False,isRightVisited=False):
        self.w = w
        self.v = v
        self.left = left
        self.right = right
        self.parent = parent
        self.isLeftVisited = isLeftVisited
        self.isRightVisited = isRightVisited


def jumpup(node):
    global index,C,V,record,tmprec
    tmp = node.parent
    if tmp == None:
        #print("@TOP\n")
        if node.isRightVisited == True:
            #print(record)
            i = max(recordV)
            ii = recordV.index(i)
            print(record[ii],i)
            exit()
        else:
            jumpdown(node)
    else:
        #print("back %d~%d cancel %d %d"%(index,index-1,w[index-1],v[index-1]))
        index -= 1
        if tmp.isLeftVisited == True and tmp.isRightVisited == False:
                tmprec = tmprec[:-1]
                C += w[index]
                V -= v[index]
            #print("\tC:%d V:%d"%(C,V))
        jumpdown(tmp)

def jumpdown(node):
    global index,w,v,C,V,res,tmprec,record,recordV,iindex
    if index >= len(w):
        #recordV = iindex if V > recordV else recordV
        #x = copy.deepcopy(tmprec) if V > recordV else []
        #print(tmprec,x)
        record.append(tmprec)
        recordV.append(V)
        jumpup(node)
    tmp = None
    if node.left == None and C-w[index]>=0:
        #print("left %d~%d add %d %d"%(index,index+1,w[index],v[index]))
        node.left = tree(w[index],v[index],parent=node)
        node.isLeftVisited = True
        V += v[index]
        C -= w[index]
        tmp = node.left
        index += 1
        tmprec.append(index)
    elif node.right == None:
        #print("right %d~%d pass %d %d"%(index,index+1,w[index],v[index]))
        node.right = tree(node.w,node.v,parent=node)
        node.isRightVisited = True
        tmp = node.right
        index += 1
    else:
        jumpup(node)
    jumpdown(tmp)

record = []
recordV = []
iindex = 0
tmprec = []
index = 0
V = 0

if __name__ == "__main__":
    root = tree(0, 0)
    print("W List:")
    w = [int(n) for n in input().split()]
    print("V List:")
    v = [int(n) for n in input().split()]
    print("C:")
    C = int(input())
    print("Result:")
    jumpdown(root)

'''
W List:
2 5 4 2
V List:
6 3 5 4
C:
8
Result:
[1, 3, 4] 15
'''