from abc import ABC
class File():
    def __init__(self, name:str, size:int):
        self.name = name
        self.size = size
        self.isDirectory = False if "." in self.name else True
        self.children = []
        if "." in self.name:
            self.extension = self.name.split(".")[1]
            self.fileName = self.name.split(".")[0]
        else:
            self.extension = None
            self.fileName = self.name

class Filter(ABC):
    def __init__(self):
        pass
    
    def search(self, file):
        pass
    
class NameFilter(Filter):
    def __init__(self, file):
        self.file = file
    
    def search(self,file: File):
        return self.file == file.fileName

class MinSizeFilter(Filter):
    def __init__(self, size):
        self.size = size
    
    def search(self,file: File):
        return file.size >= self.size

class ExtensionFilter(Filter):
    def __init__(self, extension):
        self.extension = extension
    
    def search(self,file: File):
        return file.extension == self.extension

class LogicalFilters(Filter):
    def __init__(self):
        pass
    
    def addFilter(self, filter:Filter):
        pass
    
    def getFilesFromDirectory(self, directory:str):
        pass

class AndFilter(Filter):
    def __init__(self, filterSet=None):
        self.filterSet = filterSet if filterSet is not None else set()
    
    def addFilter(self, filter:Filter):
        self.filterSet.add(filter)
    
    def search(self,file:File):
        for filter in self.filterSet:
            if not filter.search(file):
                return False
        return True

class ORFilter(Filter):
    def __init__(self, filterSet=None):
        self.filterSet = filterSet if filterSet is not None else set()
    
    def addFilter(self, filter:Filter):
        self.filterSet.add(filter)
    
    def search(self,file:File):
        for filter in self.filterSet:
            if filter.search(file):
                return True
        return False

class FileSearchEngine():
    # can add create directory and attach files as children
    def createFile(self, name, size):
        file = File(name,size)
        print("Create file with name:%s and size:%s", name,size)
        return file
    
    def getFilesFromDirectory(self, directory:str, filterRule:Filter=None) -> list:
        files = list()
        def dfs(root:File):
            for child in root.children:
                if child.isDirectory:
                    dfs(child)
                else:
                    if filterRule is None or filterRule.search(child):
                        files.append(child)
                    
        dfs(directory)
        return files

fileSearchEngine = FileSearchEngine()

directory = fileSearchEngine.createFile("root",4)
directory1 = fileSearchEngine.createFile("root1",5)

file1 = fileSearchEngine.createFile("abc.txt",3)
file2 = fileSearchEngine.createFile("abcde.png",5)
file3 = fileSearchEngine.createFile("abcdef.png",6)

directory.children = [directory1,file1,file2]
directory1.children = [file3]

#initial test
result = fileSearchEngine.getFilesFromDirectory(directory)

nameFilter = NameFilter("abcdef")
extensionFilter = ExtensionFilter("png")

andFilter = AndFilter()

andFilter.addFilter(nameFilter)
andFilter.addFilter(extensionFilter)

#result = fileSearchEngine.getFilesFromDirectory(directory, andFilter)
print("Files Found: ")

for file in result:
    print(file.name)
    
