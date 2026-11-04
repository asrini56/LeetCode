class Solution:
    def numberOfSequence(self, n: int, sick: list[int]) -> int:
        MOD = 10**9 + 7
        
        # Factorial precomputation
        fac = [1] * (n + 1)
        for i in range(2, n + 1):
            fac[i] = (fac[i - 1] * i) % MOD
            
        def nCr(N, R):
            if R < 0 or R > N:
                return 0
            return fac[N] * pow(fac[R], MOD - 2, MOD) * pow(fac[N - R], MOD - 2, MOD) % MOD

        # Collect segment lengths
        segments = []
        middle_segments = []
        
        # Left end segment
        if sick[0] > 0:
            segments.append(sick[0])
            
        # Middle segments
        for i in range(len(sick) - 1):
            gap = sick[i + 1] - sick[i] - 1
            if gap > 0:
                segments.append(gap)
                middle_segments.append(gap)
                
        # Right end segment
        if sick[-1] < n - 1:
            segments.append(n - 1 - sick[-1])
            
        total_uninfected = sum(segments)
        
        # Multinomial coefficient calculation: S! / prod(seg!)
        ans = fac[total_uninfected]
        for seg in segments:
            ans = (ans * pow(fac[seg], MOD - 2, MOD)) % MOD
            
        # Multiply by 2^(length - 1) for each middle segment
        for seg in middle_segments:
            if seg > 1:
                ans = (ans * pow(2, seg - 1, MOD)) % MOD
                
        return ans
