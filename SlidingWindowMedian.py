#Time - O(NlogK)
class SlidingWindowMedian:
    def __init__(self):
        self.max_heap = []  # max heap to store smaller numbers, get largest of small numbers
        self.min_heap = []  # min heap to store larger numbers, get smallest of large numbers

    def find_median_in_sliding_window(self, nums, k):
		result = [0.0 for _ in range(len(nums) - k + 1)] # avoid getting index out of bound error later on if initialized as empty

        for i in range(0, len(nums)):
			# negative sign for max heap since python has min heap by default, so negative sign is to simulate the proposed max heap!
			# basically remember: 
			# - Add negative sign before the number when adding to max heap!
			# - Put back the negative sign while popping the number!
			# - Keep the sign in while comparing the top element of max heap to any number!
            if not self.max_heap or nums[i] <= -self.max_heap[0]:
                heappush(self.max_heap, -nums[i])
            else:
                heappush(self.min_heap, nums[i])

            # re-balance heaps after inserting every number in the heaps
            self.rebalance_heaps()

            # if we have at least "k" elements in the sliding window
            if i - k + 1 >= 0:
                # add the median to the resulting array
                if len(self.max_heap) == len(self.min_heap):
                    # we got even number of elements, take avg of the top of the element from both heaps
                    result[i-k+1] = (self.min_heap[0] + (- self.max_heap[0])) / 2.0
                else:
                    # get the top element from the max heap
                    result[i-k+1] = -self.max_heap[0] / 1.0

                # remove the element going out of the window, from the heap
                element_to_remove = nums[i-k+1]
                if element_to_remove <= -self.max_heap[0]:
                    self.remove_element_from_heap(self.max_heap, -element_to_remove)
                else:
                    self.remove_element_from_heap(self.min_heap, element_to_remove)

                # re-balance the heaps after element removal
                self.rebalance_heaps()

        return result

    @staticmethod
    def remove_element_from_heap(heap, element):
        # find the index of the element to remove from the heap
        index = heap.index(element)
        # move this indexed element to the end of the heap to remove it
        heap[index] = heap[-1]  # this basically overrides the element at index to that of last element
        # now remove the last element, thereby removing the indexed element (because of previous step)
        del heap[-1]

        # adjust only one element instead of using heapify (heapify takes O(K), this takes O(Log K))
        if index < len(heap):
            heapify(heap)
            # TODO, understand this better
            # heapq._siftup(heap, index)
            # heapq._siftdown(heap, 0, index)

    def rebalance_heaps(self):
        # either both the heaps will have equal number of elements or max-heap will have
        # one more element than the min-heap
        if len(self.max_heap) > len(self.min_heap) + 1:
            heappush(self.min_heap, -heappop(self.max_heap))
        elif len(self.max_heap) < len(self.min_heap):
            heappush(self.max_heap, -heappop(self.min_heap))
