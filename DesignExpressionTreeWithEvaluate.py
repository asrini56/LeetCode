#Factory Pattern
import abc 
from abc import ABCMeta, abstractmethod 
"""
This is the interface for the expression tree Node.
You should not remove it, and you can define some classes to implement it.
"""

class Node:
    __metaclass__ = ABCMeta
    
    IS_OPERATOR = True
    
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    # define your fields here
    @abstractmethod
    def evaluate(self):
        pass
    
class MultiplicationNodeImpl(Node):
    
    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()

class AdditionNodeImpl(Node):
    
    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()

class SubtractionNodeImpl(Node):
    
    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()
    
class DivisionNodeImpl(Node):
    
    def evaluate(self):
        return int(self.left.evaluate() // self.right.evaluate())
    
class DataNodeImpl(Node):
    
    IS_OPERATOR = False
    
    def evaluate(self):
        return int(self.val)
    
class NodeFactory(object):
    
    IMPL_MAP = {"*":MultiplicationNodeImpl,"/":DivisionNodeImpl,"+":AdditionNodeImpl,"-":SubtractionNodeImpl}
    
    @staticmethod
    def getNode(val, left=None, right=None):
        return NodeFactory.IMPL_MAP.get(val, DataNodeImpl)(val, left, right)


"""    
This is the TreeBuilder class.
You can treat it as the driver code that takes the postinfix input
and returns the expression tree represnting it as a Node.
"""

class TreeBuilder(object):
    
    def build(self, postfix):
        if not postfix:
            return None
        if not NodeFactory.IMPL_MAP.get(postfix[-1]):
            return NodeFactory.getNode(postfix.pop())
        root = NodeFactory.getNode(postfix.pop())
        root.right = self.build(postfix)
        root.left = self.build(postfix)
        return root
    
    def buildTree(self, postfix):
        """
        
        make the last node root, then build the rest of the tree, immediate one goes on the right
        if isOperator, pop next two and keep doing the same thing
        else return it
        
        :type s: List[str]
        :rtype: int
        """
        root = self.build(postfix)
        return root
"""
Your TreeBuilder object will be instantiated and called as such:
obj = TreeBuilder();
expTree = obj.buildTree(postfix);
ans = expTree.evaluate();
"""
