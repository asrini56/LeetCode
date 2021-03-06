#21. Merge Two Sorted Lists
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        head,head1 = l1,l2
        res = ListNode(-1)
        ans = res
        while head and head1:
            if head.val <= head1.val:
                ans.next= head
                head = head.next
            else:
                ans.next = head1
                head1 = head1.next
            ans = ans.next
        if head:
            while head:
                ans.next = head
                head = head.next
                ans = ans.next
        if head1:
            while head1:
                ans.next = head1
                head1 = head1.next
                ans = ans.next
        
        return res.next
            
