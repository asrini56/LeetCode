def binarySearchRight(stIdx,endIdx,arr,target) -> int:
    ans = -1
    while stIdx <= endIdx:
        middle = (stIdx+endIdx) // 2

        if arr[middle][1] <= target:
            ans = middle
            stIdx = middle+1
        else:
            endIdx = middle-1
    return ans

def binarySearchLeft(stIdx,endIdx,arr,target) -> int:
    ans = -1
    while stIdx <= endIdx:
        middle = (stIdx+endIdx) // 2

        if arr[middle][1] >= target:
            ans = middle
            endIdx = middle-1
        else:
            stIdx = middle+1
    return ans

def findCustomerId(customerIdList : list[list], timestamp:list[int]) -> list[int]:
    result = []
    customerIdList.sort(key=lambda x:x[1])
    print(customerIdList)
    stIdx = timestamp[0]
    endIdx = timestamp[1]
    searchIdxst = binarySearchLeft(0,len(customerIdList)-1,customerIdList, stIdx)
    searchIdxend = binarySearchRight(0,len(customerIdList)-1,customerIdList, endIdx)

    temp = {}

    for i in range(searchIdxst, searchIdxend+1):
        customerId,timestamp = customerIdList[i]
        temp[customerId] = temp.get(customerId,0)+1
    
    for customer_id,count in temp.items():
        if count > 1:
            result.append(customer_id)


    return result

if __name__ == "__main__":
    # Format: [customer_id, timestamp]
    access_logs = [
        [101, 15],  
        [102, 30],  # In range
        [101, 45],  # In range (1st for 101)
        [103, 50],  # In range
        [101, 55],  # In range (2nd for 101 -> qualifies)
        [102, 65],  # In range (2nd for 102 -> qualifies)
        [104, 75],  
        [101, 95],  # In range (3rd for 101)
        [105, 120] 
    ]
    
    target_range = [25, 100]
    
    qualified_customers = findCustomerId(access_logs, target_range)
    print("Customers with >1 access in range:", qualified_customers)
 

