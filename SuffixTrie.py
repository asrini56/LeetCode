class Trie:
    def __init__(self,string):
        self.root = {}
        self.endSymbol = "*"
        self.populate(string)
    
    #O(n^2) Time and Space
    def populate(self,string):
        for i in range(len(string)):
            self.insertAtSubstring(i,string)
    
    def insertAtSubstring(self,i,string):
        node = self.root
        for j in range(i,len(string)):
            letter = string[j]
            if letter not in node:
                node[letter] = {}
            node = node[letter]
        node[self.endSymbol] = True
    
    #O(m) time where m is search string length, space - O(1)   
    def contains(self,string):
        node = self.root
        for letter in string:
            if letter not in node:
                return False
            node = node[letter]
        return self.endSymbol in node
string = "ashwin"
trie = Trie(string)
print(trie.contains("win"))
