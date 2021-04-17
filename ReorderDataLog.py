#937. Reorder Data in Log Files, Time - O(M⋅N⋅logN), Space - O(M.N)
class Solution:
    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        def get_key(log):
            i,rest = log.split(" ",maxsplit = 1)
            if rest[0].isalpha():
                return (0,rest,i)
            else:
                return (1, )
        
        return sorted(logs,key=get_key)
