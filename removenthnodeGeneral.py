#19. Remove Nth Node From End of List, Time -O(n)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        count = 0
        curr = head
        ans = ListNode(-1)
        ans.next = head
        while curr:
            curr = curr.next
            count+=1
        node = count - n
        curr = ans
        while node > 0:
            print(node)
            curr = curr.next
            node-=1
        curr.next = curr.next.next
        return ans.next
