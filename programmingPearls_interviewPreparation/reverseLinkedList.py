
class Node:
	def __init__(self, value, next=None):
		self.value = value
		self.next = next
	def toList(self):
		return [self.value] + (self.next.toList() if self.next else [])

def reverseLinkedListMutable(head):
	if not head:
		return head
	else:
		previous = None
		while (head.next):
			current = head
			head = head.next
			current.next = previous
			previous = current
		head.next = previous
		return head

A = Node(1, Node(2, Node(3)))
A.toList()

R = reverseLinkedListMutable(A)
R0 = reverseLinkedListMutable(None)
R1 = reverseLinkedListMutable(Node(1))
R2 = reverseLinkedListMutable(Node(1, Node(2)))

R0 == None
R1.toList() == [1]
R2.toList() == [2,1]