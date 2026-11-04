from typing import List

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Calculates the minimum units of time required to finish all tasks 
        given a cooling period 'n' between identical tasks.
        
        Example Walkthrough:
        -------------------
        tasks = ["A", "A", "A", "B", "B", "B"], n = 2
        
        1. Frequency Counting:
           - Count frequencies: A: 3, B: 3
           - Sorted frequencies end with: [..., 3, 3]
           
        2. Initial Idle Time Calculation:
           - Most frequent task is A (freq = 3).
           - maximum = freq[25] - 1 = 3 - 1 = 2 chunks/gaps.
           - Initial idle_time = maximum * n = 2 * 2 = 4 slots.
           - Visual layout so far: A _ _ A _ _ A  (4 idle slots to fill)
           
        3. Filling Idle Slots with Remaining Tasks:
           - Next task is B (freq = 3).
           - min(maximum, freq[24]) = min(2, 3) = 2.
           - idle_time -= 2 -> idle_time becomes 4 - 2 = 2.
           - B fills 2 idle slots: A B _ A B _ A
           
        4. Final Result:
           - Since idle_time (2) > 0, total time = len(tasks) + idle_time
           - 6 + 2 = 8 units.
           - Final schedule: A B X A B X A B (where X is idle)
        """
        # Step 1: Count frequency of each task (A-Z)
        freq = [0] * 26
        for task in tasks:
            freq[ord(task) - ord('A')] += 1
        
        # Step 2: Sort frequencies so the highest frequency is at the end (freq[25])
        freq.sort()
        
        # Step 3: Calculate initial idle slots based on the most frequent task
        maximum = freq[25] - 1
        idle_time = maximum * n

        # Step 4: Subtract slots filled by all other tasks
        for i in range(24, -1, -1):
            # A task can fill at most 'maximum' slots (one per chunk)
            idle_time -= min(maximum, freq[i])
        
        # Step 5: Return total time (total tasks + remaining idle time, if any)
        return idle_time + len(tasks) if idle_time > 0 else len(tasks)

# --- Example Usage & Validation ---
sol = Solution()

tasks1 = ["A", "A", "A", "B", "B", "B"]
n1 = 2
print(f"Tasks: {tasks1}, n: {n1}")
print(f"Least intervals required: {sol.leastInterval(tasks1, n1)}")  # Output: 8

tasks2 = ["A", "A", "A", "B", "B", "B"]
n2 = 0
print(f"\nTasks: {tasks2}, n: {n2}")
print(f"Least intervals required: {sol.leastInterval(tasks2, n2)}")  # Output: 6
