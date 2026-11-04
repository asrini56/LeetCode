class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        if not headA or not headB:
            return None
        
        pA = headA
        pB = headB
        
        # Loop until pointers meet or both become None
        while pA != pB:
            # If pA reaches the end, switch to headB; otherwise, move to next
            pA = pA.next if pA else headB
            # If pB reaches the end, switch to headA; otherwise, move to next
            pB = pB.next if pB else headA
            
        # Return either the intersection node or None
        return pA
