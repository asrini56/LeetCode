class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        """
        Floyd's Tortoise and Hare Algorithm (Cycle Detection)
        ----------------------------------------------------
        Concept: Treat the array as a Linked List where index `i` points to value `nums[i]`.
        Because the array contains n + 1 numbers ranging from 1 to n, the duplicate 
        number creates a shared destination (merge point), which guarantees a cycle.
        """
        
        # -------------------------------------------------------------------------
        # PHASE 1: Detect the cycle and find the meeting point inside it
        # -------------------------------------------------------------------------
        # Both runners start at the first element's value (nums[0]).
        tortoise = nums[0]
        hare = nums[0]

        while True:
            # Tortoise moves 1 step forward: index -> nums[index]
            tortoise = nums[tortoise]       
            # Hare moves 2 steps forward: index -> nums[index] -> nums[nums[index]]
            hare = nums[nums[hare]]         
            
            # Because of the cycle, the fast hare will eventually lap and 
            # collide with the slow tortoise.
            if tortoise == hare:
                break
        
        # -------------------------------------------------------------------------
        # PHASE 2: Find the entrance of the cycle (the duplicate number)
        # -------------------------------------------------------------------------
        # Mathematical proof shows that the distance from the start of the array 
        # to the cycle entrance equals the distance from the collision point to 
        # the cycle entrance.
        
        p1 = nums[0]       # Place pointer 1 back at the very beginning
        p2 = tortoise      # Keep pointer 2 at the collision point from Phase 1

        # Move both pointers at the exact same speed (1 step at a time).
        # Where they meet is the start of the cycle — our duplicate number!
        while p1 != p2:
            p1 = nums[p1]
            p2 = nums[p2]
        
        return p1

# Example Walkthrough:
if __name__ == "__main__":
    solution = Solution()
    
    # Input: nums = [1, 3, 4, 2, 2]
    # Visualized as a linked list (Index -> Value):
    # Index 0 -> Value 1
    # Index 1 -> Value 3
    # Index 2 -> Value 4
    # Index 3 -> Value 2
    # Index 4 -> Value 2  <-- (Notice both index 3 and 4 point to 2, forming a loop)
    
    nums = [1, 3, 4, 2, 2]
    result = solution.findDuplicate(nums)
    
    print(f"Input: {nums}")
    print(f"Found Duplicate: {result}")  # Output: 2
