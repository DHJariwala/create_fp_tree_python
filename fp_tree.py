# IMPORT PACKAGES
import subprocess
import sys

# INSTALL AND IMPORT PACKAGES
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def installPackages(packages):
    for package in packages:
        install(package)

packages = ['anytree']

try:
    from anytree import Node,RenderTree
    from anytree.exporter import DotExporter
except:
    installPackages(packages)
    from anytree import Node,RenderTree
    from anytree.exporter import DotExporter
    pass

# INPUTS
n = int(input())
transaction = []
for _ in range(n):
    transaction.append(input().split())
    pass

# VARIABLES
minsup = 3
freqCounter = {}
frequentItems = {}
flist = []
tmpOrderedTransaction = []
orderedTransaction = []

# FUNCTIONS
def splitName(name):
    x = name.split()
    return x[0]

def splitFreq(name):
    x = name.split()
    return x[1]

def printTree(tree):
    print(RenderTree(tree).by_attr())
    pass

def print2DArray(arr):
    for x in arr:
        print(x) 

# FREQUENCY COUNTER
for x in transaction:
    for item in x:
        if item in freqCounter:
            freqCounter[item] += 1
        else:
            freqCounter[item] = 1
            pass
        pass
    pass

# ELIMINATING ITEMS THAT HAVE FREQUENCY LESS THEN MINSUP
for item in freqCounter:
    if freqCounter[item] >= minsup:
        frequentItems[item] = freqCounter[item]

# SORT THESE ITEMS ACCORDING TO VALUE
sortedFreq = sorted(frequentItems.items(), key=lambda x: x[1], reverse=True)

# CREATE F-LIST
for item in sortedFreq:
    flist.append(item[0])

# ORDER THE TRANSACTIONS ACCORDING TO F-LIST
for trans in transaction:
    tmp = []
    for item in trans:
        if item in flist:
            tmp.append(item)
    tmpOrderedTransaction.append(tmp)
    pass
for trans in transaction:
    tmp = []
    for oitem in flist:
        if oitem in trans:
            tmp.append(oitem)
    orderedTransaction.append(tmp)
    pass
# UNCOMMENT THE LINE BELOW TO DISPLAY THE ORDERED TRANSACTIONS (ACCORDING TO F-LIST)
# print2DArray(orderedTransaction)

#  MAKING F-TREE
root = Node('root')
for trans in orderedTransaction:
    currentNode = root
    for item in trans:
        if currentNode.children == ():
            newNode = Node(item + ' 1',parent=currentNode)
            currentNode = newNode
        else:
            tmp = list(currentNode.children)
            nodeLoc = 0
            flag = 1
            for sibling in tmp:
                if splitName(sibling.name) == item:
                    ttmp = tmp[nodeLoc].children
                    newNode = Node(item + ' ' + str(int(splitFreq(sibling.name))+1),
                                   parent=currentNode,
                                   children=ttmp)
                    tmp[nodeLoc] = newNode
                    currentNode.children = tmp
                    currentNode = newNode
                    flag = 0
                    pass
                nodeLoc += 1
            if flag:
                newNode = Node(item + ' 1',parent=currentNode)
                tmp.append(newNode)
                currentNode.children = tmp
                currentNode = newNode
                pass
            pass
        pass
    pass

# PRINT THE TREE (RESULT)
printTree(root)