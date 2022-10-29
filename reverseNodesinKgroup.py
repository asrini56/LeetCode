#25. Reverse Nodes in k-Group, Time - O(N+k)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        dummy = ListNode(-1,head)
        groupPrev = dummy
        curr = head
        while True:
                kthNode = self.getKthNode(groupPrev,k)
                if not kthNode:
                    break
                groupNext = kthNode.next
                prev = kthNode.next
                curr = groupPrev.next
                while curr != groupNext:
                    temp = curr.next
                    curr.next = prev
                    prev = curr
                    curr = temp
                temp = groupPrev.next
                groupPrev.next = kthNode
                groupPrev = temp
        return dummy.next
    def getKthNode(self,curr,k):
        while curr and k > 0:
            curr = curr.next
            k-=1
        return curr
