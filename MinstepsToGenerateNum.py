from collections import deque
def num_steps(n):
  # initialize queue with 1
  queue = deque([1])
  no_of_steps = 0

  while(queue):
    no_of_elements_to_remove = len(queue)

    no_of_steps += 1

    for i in range(no_of_elements_to_remove):
      cur_number = queue.popleft()

      muliply_by_2 = int(cur_number * 2) 
      divide_by_3 = int(cur_number / 3)

      if(muliply_by_2 == n or divide_by_3 == n): return no_of_steps

      # append multiplication and division results to queue
      queue.append(muliply_by_2)
      if(divide_by_3 > 0): queue.append(divide_by_3)
print(num_steps(11))
