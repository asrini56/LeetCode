def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        plus = []
        minus = []
        for a in asteroids:
            if a > 0:
                plus.append(a)
            else:
                while plus and plus[-1] < abs(a):
                    plus.pop()
                if not plus:
                    minus.append(a)
                elif plus[-1] == abs(a):
                    plus.pop()
                
        return minus + plus
