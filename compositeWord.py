def compositeWord(word,s):  
    if not word:
        return True  
    for prefix in (word[:i] for i in range(1, len(word) + 1)):
        if prefix in s:
            if compositeWord(word[len(prefix):], s) == True:
                return True         
    s.add(word)    
    return False       

def simpleWords(words):    
    s = set()   
    return [w for w in words if not compositeWord(w,s)]

if __name__ == '__main__': 
    print(simpleWords(sorted(["chat","ever","snapchat","snap","salesperson","per","person","sales","son","whatsoever","what","so"],key=lambda s: len(s))))
