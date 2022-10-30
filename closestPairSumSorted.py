# Python3 program to find the pair from
# two sorted arrays such that the sum
# of pair is closest to a given number x
import sys

# ar1[0..m-1] and ar2[0..n-1] are two
# given sorted arrays and x is given
# number. This function prints the pair
# from both arrays such that the sum
# of the pair is closest to x.
def printClosest(ar1, ar2, m, n, x):

	# Initialize the diff between
	# pair sum and x.
	diff=sys.maxsize

	# res_l and res_r are result
	# indexes from ar1[] and ar2[]
	# respectively. Start from left
	# side of ar1[] and right side of ar2[]
	l = 0
	r = n-1
	while(l < m and r >= 0):
	
	# If this pair is closer to x than
	# the previously found closest,
	# then update res_l, res_r and diff
		if abs(ar1[l] + ar2[r] - x) < diff:
			res_l = l
			res_r = r
			diff = abs(ar1[l] + ar2[r] - x)
	

	# If sum of this pair is more than x,
	# move to smaller side
		if ar1[l] + ar2[r] > x:
			r=r-1
		else: # move to the greater side
			l=l+1
	

	# Print the result
	print("The closest pair is [",
		ar1[res_l],",",ar2[res_r],"]")

# Driver program to test above functions
ar1 = [1, 4, 5, 7]
ar2 = [10, 20, 30, 40]
m = len(ar1)
n = len(ar2)
x = 38
printClosest(ar1, ar2, m, n, x)
