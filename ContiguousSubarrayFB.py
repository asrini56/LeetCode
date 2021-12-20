def count_subarrays(arr):
  # Write your code here
  res = [1] * len(arr)
  stack = [-1]
  n = len(arr)
  for i in range(len(arr)):
    print(stack)
    while len(stack) > 1 and arr[stack[-1]] < arr[i]:
      stack.pop()
    res[i] += i - stack[-1] - 1
    stack.append(i)
  
  # from right
  stack = [len(arr)]
  for i in range(n - 1, -1, -1):
    while len(stack) > 1 and arr[stack[-1]] < arr[i]:
      stack.pop()
    res[i] += stack[-1] - i - 1
    stack.append(i)
  return res
