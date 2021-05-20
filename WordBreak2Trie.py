#140. Word Break II, time - 0(n^2 + 2^n + w)
"""
N be the length of the input string and WW be the number of words in the dictionary.
"""
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        all_results = []
        trie = {}
        s_letters, words_letters = set(s), set()

        # Build a trie from the words in word dictionary
        for word in wordDict:
            node = trie

            for letter in word:
                if letter not in node:
                    node[letter] = {}
                node = node[letter]
                words_letters.add(letter)

            node[None] = word

        # Check if all letters of the S string are in the words' letters
        if s_letters - words_letters:
            return []

        # BFS
        # Each element in the queue is the S-string index (current parsing position) and
        # an array with the found words so far
        queue = collections.deque([(0, [])])

        while queue:
            idx, result = queue.pop()

            # If index has reached the end of the S string, then we have found one of the
            # results
            if idx == len(s):
                all_results.append(" ".join(result))
                continue

            # Go through the trie until a word is found
            node = trie

            while idx < len(s) and s[idx] in node:
                node = node[s[idx]]
                idx = idx + 1

                if None in node:
                    queue.append((idx, result + [node[None]]))

        return all_results
