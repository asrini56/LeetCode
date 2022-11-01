"""
Time: O(T + M * L)
O(T) for building Trie structure with all products, where T <= 2*10^4 is total number of characters in products.
O(M * L): In worst case, dfs to search up to 3 products can run up to O(L), where L is the length of the word which has largest length. We need to dfs up to M times, where M <= 1000 is length of searchWord.
Total time complexity: O(T + M * L).
Space: O(T), it's total number of characters in the worst case when building Trie structure.
"""
class TrieNode:
    def __init__(self):
        self.word = None
        self.child = defaultdict(TrieNode)

    def addWord(self, word):
        curr = self
        for c in word:
            curr = curr.child[c]
        curr.word = word

    def getWords(self, limit):
        words = []

        def dfs(curr):
            if len(words) == limit: return
            if curr.word != None:
                words.append(curr.word)
            for c in ascii_lowercase:
                if c in curr.child:
                    dfs(curr.child[c])

        dfs(self)
        return words

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        root = TrieNode()
        for product in products:
            root.addWord(product)

        ans = []
        curr = root
        for c in searchWord:
            if curr != None and c in curr.child:
                curr = curr.child[c]
                ans.append(curr.getWords(3))
            else:
                curr = None
                ans.append([])
        return ans
