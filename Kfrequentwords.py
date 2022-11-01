def topKFrequent(self, words: List[str], k: int) -> List[str]:
        # so first we create a count dictionary/ hashmap to count our frequency O(n)
        count = {}
        for word in words:
             count[word] = count.get(word, 0) + 1
        # Then we make an abstract minheap (which is a list) and populate the list with all the values O(n)
        minheap =[]
        for word, counter in count.items():
            minheap.append((-counter, word))
        # Now using this list we manipulate it to a minheap that acts like a max heap by using negative "-counter". O(n)
        heapq.heapify(minheap)
        
        # Then as "pizarro" mentioned below. heappop pops elements lexicographically O(k log n)
        output = []
        for i in range(k):
            output.append(heapq.heappop(minheap)[1])
      
        return output
# T: O(k log n)
# S: O(n)
