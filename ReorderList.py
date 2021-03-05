#143. Reorder List, Time - O(n), Space - O(1)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: ListNode) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if not head:
            return 
        
        #Middle of Linked List
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next 
        
        #Reverse a Linked List
        prev,curr = None,slow
        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        
        #Merge Linked List
        first,second = head,prev
        while second.next:
            first.next,first = second,first.next
            second.next,second = first,second.next
