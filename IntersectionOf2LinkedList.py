#160. Intersection of Two Linked Lists, Time - O(n)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        dict1 = {}
        head1 = headA
        head2 = headB
        while head1:
            if head1 not in dict1:
                dict1[head1] = id(head1)
            head1 = head1.next
        while head2:
            if head2 in dict1.keys():
                return head2
            head2 = head2.next
        return None
            
