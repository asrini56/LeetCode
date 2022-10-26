#Time - O(n)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def rotateRight(self, head: ListNode, k: int) -> ListNode:
        if not head:
            return None
        curr = head
        ans = head
        prev = None
        count = 1
        while curr.next:
            curr = curr.next
            count+=1
        if k%count == 0:
            return head
        temp = count - k
        for i in range(count-k%count-1):
            ans = ans.next
        newHead = ans.next
        curr.next = head
        ans.next = None
        return newHead
