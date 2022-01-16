#621. Task Scheduler, Time - O(n), Space - O(1)
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        freq = [0] * 26
        for task in tasks:
            freq[ord(task) - ord('A')]+=1
        freq.sort()
        fmax = freq.pop()
        idle_time = (fmax - 1) * n
        
        while idle_time and freq:
            print(idle_time,freq)
            idle_time -= min(freq.pop(),fmax-1)
        idle_time = max(0,idle_time)
        return idle_time + len(tasks)
    
    """
    working:
    tasks = ["A","A","A","B","B","B"], n = 2
    freq = [3,3]
    freq.sort() = [0,0,.....3,3]
    fmax = 3
    idle = 4 [(3-1)*2]
    while idle and freq:
        1] idle -= min(3,2) = idle = 2
        ...
    idle = max(idle,0) = 2
    ans = 2 + 6 = 8
    
    
    
    freq = collections.Counter(tasks).values()
        maxFreq = max(freq)
        maxFreqCount = freq.count(maxFreq)
            
        ans = (maxFreq - 1) * (n+1) + maxFreqCount
        
        return max(ans, len(tasks))
    """
