class Solution:
    def fractionToDecimal(self, num: int, denom: int) -> str:
        """
        n = 4, d = 333
        40 {4: 0} 40 0
        400 {4: 0, 40: 1} 67 01
        670 {4: 0, 40: 1, 67: 2} 4 012

        """
        ##first check if it goes evenly
        if num % denom == 0:
            return str(num//denom)
        
        ##otherwise we gotta get the integral part and decimal part
        sign = '' if num*denom >=0 else '-'
        ##easier to start with positive values
        num = abs(num)
        denom = abs(denom)
        
        ##init rest with sign and intergral part
        res = sign+str(num//denom)+"."
        
        ##start off with remainder
        num = num % denom
        i = 0
        part = ''
        
        m = {num:i} ##the remainder and position
        
        while num % denom != 0: #while there is a reaminder
            ##add zeros digit
            num *= 10
            i += 1
            rem = num % denom
            part += str(num // denom)
            print(num,m,rem,part)
            ##if we have seen this remainder, build it part and return
            if rem in m:
                ##we've repeated up this part so first find the non repreating part
                non_repeating = part[:m[rem]]
                repeating = part[m[rem]:]
                return res + non_repeating + '('+repeating+')'
            ##other mark as new
            m[rem] = i
            num = rem
        
        ##must be non repeating in remainder
        return res + part
