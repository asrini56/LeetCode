import collections

class TrieNode:
    def __init__(self):
        self.children = {}
        self.words = []

class AutoCompleteSystem:
    def __init__(self, sentences: list[str], times: list[int]):
        self.root = TrieNode()
        self.cache_count = collections.defaultdict(int)
        self.keyword = ""
        
        for sentence, time in zip(sentences, times):
            self.cache_count[sentence] = time
            self.addWord(sentence)
    
    def addWord(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            # Avoid duplicate entries if the word is added again
            if word not in node.words:
                node.words.append(word)
    
    def search(self, prefix: str) -> list[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  # Prefix does not exist in the Trie
            node = node.children[char]
        return node.words
    
    def query(self, s: str) -> list[str]:
        if s == "#":
            # Save the completed keyword and update its frequency
            if self.keyword:
                self.cache_count[self.keyword] += 1
                self.addWord(self.keyword)
            self.keyword = ""
            return []
        else:
            self.keyword += s
            words = self.search(self.keyword)
            
            res = []
            for word in words:
                res.append((self.cache_count[word], word))
            
            # Sort by highest frequency descending, then lexicographically ascending
            res.sort(key=lambda x: (-x[0], x[1]))
            res = res[:3]  # Keep top 3
            
            return [word for _, word in res]

# Test Case
sentences = ["i love you", "ironman", "i love you more", "island"]
times = [5, 2, 3, 2]
autoCompleteSystem = AutoCompleteSystem(sentences, times)
print(autoCompleteSystem.query("i"))
# Output: ['i love you', 'i love you more', 'ironman']
