class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        if len(flowerbed) == 1:
            if flowerbed[0] == 0:
                n-=1
        for i in range(len(flowerbed)):
            if n == 0:
                break
            if i == 0 and i+1 < len(flowerbed) and flowerbed[i] == 0:
                if flowerbed[i+1] == 0:
                    flowerbed[i] = 1
                    n-=1
            elif i == len(flowerbed) - 1 and len(flowerbed) >= 2 and flowerbed[i] == 0:
                if flowerbed[i-1] == 0:
                    flowerbed[i] = 1
                    n-=1
            elif i != 0 and i != len(flowerbed)-1:
                if flowerbed[i-1] == 0 and flowerbed[i+1] == 0 and flowerbed[i] == 0: 
                    flowerbed[i] = 1
                    n-=1
        if n <= 0:
            return True
        return False
                    
