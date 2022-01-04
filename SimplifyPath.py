class Solution:
    def simplifyPath(self, path: str) -> str:
        
        # stack to store directory name
        stack = []
        
        
        # check each directory name in given path, split by '/'
        for dir_name in path.split('/'):
        
            if dir_name == '' or dir_name == '.':
                
                # do nothing if directory name is either empty string or '.'
                continue
                
            elif dir_name == '..':
                
                # go back to parnet level and pop stack if stack is not empty
                if stack:
                    stack.pop()
                else:
                    continue
            
            else:
                # push current directory name into stack
                stack.append(dir_name)
                
                
        return '/' + '/'.join(stack)
