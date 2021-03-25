def candy_crush(input):
    if not input:
        return input
    
    stack = []
    stack.append([input[0], 1])
    
    for i in range(1, len(input)):
        if input[i] != input[i-1]:
            if stack[-1][1] >= 3:
                stack.pop()
            if stack and stack[-1][0] == input[i]:
                stack[-1][1] += 1
            else:
                stack.append([input[i], 1])
        else:
            stack[-1][1] += 1
            
    # handle end
    if stack[-1][1] >= 3:
        stack.pop()
        
    out = []
    for ltrs in stack:
        out += ltrs[0] * ltrs[1]
    
    return ''.join(out)
    
print(candy_crush("aaaabbbc")) #c
print(candy_crush("aabbbacd")) #cd
print(candy_crush("aabbccddeeedcba")) #blank expected
print(candy_crush("aabbbaacd")) #cd
print(candy_crush("dddabbbbaccccaax")) #x
