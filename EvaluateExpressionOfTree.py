# Python program to evaluate expression tree -> Factory Pattern

# Class to represent the nodes of syntax tree
class node:
	def __init__(self, value):
		self.left = None
		self.data = value
		self.right = None
from abc import ABC
class Evaluate(ABC):
    
    def evaluate(self):
        pass

class Add(Evaluate):
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def evaluate(self):
        return self.left+self.right

class Sub(Evaluate):
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def evaluate(self):
        return self.left-self.right

class Mul(Evaluate):
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def evaluate(self):
        return self.left*self.right

class Div(Evaluate):
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def evaluate(self):
        return int(self.left//self.right)

    
class EvalFactory():
    def __init__(self,data,left,right):
        self.data = data
        self.left = left
        self.right = right
    def evaluateExp(self):
        if self.data == '+':
            add = Add(self.left,self.right)
            return add.evaluate()
        elif self.data == '-':
            add = Sub(self.left,self.right)
            return add.evaluate()
        elif self.data == '*':
            add = Mul(self.left,self.right)
            return add.evaluate()
        else:
            add = Div(self.left,self.right)
            return add.evaluate()
        

# This function receives a node of the syntax tree
# and recursively evaluate it
def evaluateExpressionTree(root):

	# empty tree
	if root is None:
		return 0

	# leaf node
	if root.left is None and root.right is None:
		return int(root.data)

	# evaluate left tree
	left_sum = evaluateExpressionTree(root.left)

	# evaluate right tree
	right_sum = evaluateExpressionTree(root.right)

	# check which operation to apply
	evalFactory = EvalFactory(root.data,left_sum,right_sum)
	return evalFactory.evaluateExp()

# Driver function to test above problem
if __name__=='__main__':
	
	# creating a sample tree
	root = node('+')
	root.left = node('*')
	root.left.left = node('5')
	root.left.right = node('4')
	root.right = node('-')
	root.right.left = node('100')
	root.right.right = node('20')
	print(evaluateExpressionTree(root))

	root = None

	#creating a sample tree
	root = node('+')
	root.left = node('*')
	root.left.left = node('5')
	root.left.right = node('4')
	root.right = node('-')
	root.right.left = node('100')
	root.right.right = node('/')
	root.right.right.left = node('20')
	root.right.right.right = node('2')
	print(evaluateExpressionTree(root))
