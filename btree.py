import pydot
b= 2
class Node:
    def __init__(self, data, par = None):
        #print ("Node __init__: " + str(data))
        self.data = list([data])
        self.parent = par
        self.child = list()
        
    def __str1__(self):
        if self.parent:
            return str(self.parent.data) + ' : ' + str(self.data)
        return 'Root : ' + str(self.data)
    
    def __lt__(self, node):
        return self.data[0] < node.data[0]
        
    def _isLeaf(self):
        return len(self.child) == 0
            
    # merge new_node sub-tree into self node
    def _add(self, new_node):
        print ("Node _add: " + str(new_node.data) + ' to ' + str(self.data))
        for child in new_node.child:
            child.parent = self
        self.data.extend(new_node.data)
        self.data.sort()
        self.child.extend(new_node.child)
        if len(self.child) > 1:
            self.child.sort()
            for child in self.child:
                child.parent = self
        if len(self.data) > b:
            self._split()
    
    # find correct node to insert new node into tree
    def _insert(self, new_node):
        print ('Node _insert: ' + str(new_node.data) + ' into ' + str(self.data))
        
        # leaf node - add data to leaf and rebalance tree
        if self._isLeaf():
            self._add(new_node)
            
        # not leaf - find correct child to descend, and do recursive insert
        elif new_node.data[0] > self.data[-1]:
            self.child[-1]._insert(new_node)
        else:
            for i in range(0, len(self.data)):
                if new_node.data[0] < self.data[i]:
                    self.child[i]._insert(new_node)
                    break
    
    # 3 items in node, split into new sub-tree and add to parent    
    def _split(self):
        print("Node _split: " + str(self.data))
        left_child = Node(self.data[0], self)
        right_child = Node(self.data[(len(self.data)//2)+1], self)
        #if len(self.data) > 2:
        for i in range(1,(len(self.data)//2)):
            left_child.data.append(self.data[i])

        for i in range((len(self.data)//2)+2,len(self.data)):
            right_child.data.append(self.data[i])  

        if self.child:
            left_child.child = []
            right_child.child = []

            for i in range((len(self.data)//2)):
                self.child[i].parent = left_child
                left_child.child.append(self.child[i])

            for i in range((len(self.data)//2)+1,len(self.data)+1):
                self.child[i].parent = right_child
                right_child.child.append(self.child[i])

            '''for i in range(len(self.data)//2):
                #self.child[i].parent = left_child
                left_child.child.append(self.child[i])

            for i in range(len(self.data)//2,len(self.data)+1):
                #self.child[i].parent = right_child
                right_child.child.append(self.child[i])'''

                    
        self.child = [left_child]
        self.child.append(right_child)
        self.data = [self.data[len(self.data)//2]]
        
        # now have new sub-tree, self. need to add self to its parent node
        if self.parent:
            if self in self.parent.child:
                self.parent.child.remove(self)
            self.parent._add(self)
        else:
            left_child.parent = self
            right_child.parent = self
            
    # find an item in the tree; return item, or False if not found      
    def _find(self, item):
        # print ("Find " + str(item))
        if item in self.data:
            return item
        elif self._isLeaf():
            return False
        elif item > self.data[-1]:
            return self.child[-1]._find(item)
        else:
            for i in range(len(self.data)):
                if item < self.data[i]:
                    return self.child[i]._find(item)


       
    def _remove(self, item):
        pass
        
    # print preorder traversal      
    def _preorder(self):
        print (self) 
        for child in self.child:
            child._preorder()
    
class Tree:
    def __init__(self):
        print("Tree __init__")
        self.root = None
        
    def insert(self, item):
        print("Tree insert: " + str(item))
        if self.root is None:
            self.root = Node(item)
        else:
            self.root._insert(Node(item))
            while self.root.parent:
                self.root = self.root.parent
        return True
    
    def find(self, item):
        return self.root._find(item)
        
    def remove(self, item):
        self.root.remove(item)
        
    def printTop2Tiers(self):
        print ('----Top 2 Tiers----')
        print (str(self.root.data))
        for child in self.root.child:
            print (str(child.data), end=' ')
        print(' ')
        
    def preorder(self):
        print ('----Preorder----')
        self.root._preorder()
        

    def traverse(self):
        thislevel = [self.root]
        while thislevel:
            nextlevel = list()
            print('\n')
            for n in thislevel:

                print (str(n.data), end=' ')
                for child in n.child:
                    nextlevel.append(child)
                print
                thislevel = nextlevel


    def graphh(self):
        
        graph = pydot.Dot(graph_type='graph')
        thislevel = [self.root]
        while thislevel:
            nextlevel = list()
            #print('\n')
            for n in thislevel:

                #print (str(n.data), end=' ')
                for child in n.child:
                    edge = pydot.Edge(str(n.data),str(child.data))
                    graph.add_edge(edge)
                    nextlevel.append(child)
                print
                thislevel = nextlevel

        graph.write_png('btee.png')
        

tree = Tree()

b = int(input('enter the value of b:'))

lst = [3, 1, 5, 4, 2, 9, 10, 8, 7, 6]
for item in lst:
    tree.insert(item)
#tree.printTop2Tiers()
tree.traverse()
tree.graphh()


# for i in range (25):
    # tree.insert(i)
    # tree.printTop2Tiers()
# tree.preorder()
# print (tree.find(16))