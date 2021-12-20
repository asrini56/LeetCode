def numberOfWays(arr, k):
   # Write your code here
  d = collections.Counter(arr)
  count = 0
  for i in range(len(arr)):
    if k - arr[i] in d:
      count = count + (d[k-arr[i]])
    if k - arr[i] == arr[i]:
      count = count - 1
  return count//2
