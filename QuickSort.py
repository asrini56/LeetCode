#Time - O(nlogn), Space - O(logn)
def quicksort(arr):
    quicksortHelper(arr,0,len(arr)-1)
    return arr

def quicksortHelper(arr,st,end):
    if st >= end:
        return
    pivot = st
    left = st + 1
    right = end
    while left <= right:
        if arr[pivot] < arr[left] and arr[right] < arr[pivot]:
            swap(left,right,arr)
            
        if arr[left] <= arr[pivot]:
            left+=1
        
        if arr[right] >= arr[pivot]:
            right-=1
        
    swap(right,pivot,arr)
    
    isleft = right - 1 - st < end - (right + 1)
    if isleft:
        quicksortHelper(arr,st,right-1)
        quicksortHelper(arr,right+1,end)
    else:
        quicksortHelper(arr,right+1,end)
        quicksortHelper(arr,st,right-1)

def swap(left,right,arr):
    arr[left],arr[right] = arr[right],arr[left]
    
arr = [3,5,2,0,10,9]
print(quicksort(arr))
