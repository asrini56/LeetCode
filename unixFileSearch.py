"""
CLASS BLUEPRINT:

1. File
   - Variables: name, size, isDirectory, children, extension, fileName
   - Methods: __init__()

2. Filter (ABC)
   - Variables: None
   - Methods: search(file: File) -> bool

3. NameFilter (inherits Filter)
   - Variables: name
   - Methods: __init__(name: str), search(file: File) -> bool

4. MinSizeFilter (inherits Filter)
   - Variables: size
   - Methods: __init__(size: int), search(file: File) -> bool

5. ExtensionFilter (inherits Filter)
   - Variables: extension
   - Methods: __init__(extension: str), search(file: File) -> bool

6. AndFilter (inherits Filter)
   - Variables: filterSet
   - Methods: __init__(filterSet), addFilter(filter: Filter), search(file: File) -> bool

7. ORFilter (inherits Filter)
   - Variables: filterSet
   - Methods: __init__(filterSet), addFilter(filter: Filter), search(file: File) -> bool

8. FileSearchEngine
   - Variables: None
   - Methods: createFile(name: str, size: int) -> File, 
              getFilesFromDirectory(directory: File, filterRule: Optional[Filter]) -> List[File]
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Set

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.isDirectory = False if "." in self.name else True
        self.children: List['File'] = []
        if "." in self.name:
            parts = self.name.split(".", 1)
            self.fileName = parts[0]
            self.extension = parts[1]
        else:
            self.fileName = self.name
            self.extension = None

class Filter(ABC):
    @abstractmethod
    def search(self, file: File) -> bool:
        pass
    
class NameFilter(Filter):
    def __init__(self, name: str):
        self.name = name
    
    def search(self, file: File) -> bool:
        return self.name == file.fileName

class MinSizeFilter(Filter):
    def __init__(self, size: int):
        self.size = size
    
    def search(self, file: File) -> bool:
        return file.size >= self.size

class ExtensionFilter(Filter):
    def __init__(self, extension: str):
        self.extension = extension
    
    def search(self, file: File) -> bool:
        return self.extension == file.extension

class AndFilter(Filter):
    def __init__(self, filterSet: Optional[Set[Filter]] = None):
        self.filterSet = filterSet if filterSet is not None else set()
    
    def addFilter(self, filter: Filter):
        self.filterSet.add(filter)
    
    def search(self, file: File) -> bool:
        for f in self.filterSet:
            if not f.search(file):
                return False
        return True

class ORFilter(Filter):
    def __init__(self, filterSet: Optional[Set[Filter]] = None):
        self.filterSet = filterSet if filterSet is not None else set()
    
    def addFilter(self, filter: Filter):
        self.filterSet.add(filter)
    
    def search(self, file: File) -> bool:
        for f in self.filterSet:
            if f.search(file):
                return True
        return False

class FileSearchEngine:
    def createFile(self, name: str, size: int) -> File:
        file = File(name, size)
        print(f"Created file with name: {name} and size: {size}")
        return file
    
    def getFilesFromDirectory(self, directory: File, filterRule: Optional[Filter] = None) -> List[File]:
        files = []
        def dfs(root: File):
            for child in root.children:
                if child.isDirectory:
                    dfs(child)
                else:
                    if filterRule is None or filterRule.search(child):
                        files.append(child)
                    
        dfs(directory)
        return files

if __name__ == '__main__':
    fileSearchEngine = FileSearchEngine()

    directory = fileSearchEngine.createFile("root", 4)
    directory1 = fileSearchEngine.createFile("root1", 5)

    file1 = fileSearchEngine.createFile("abcdef.txt", 3)
    file2 = fileSearchEngine.createFile("abcde.png", 5)
    file3 = fileSearchEngine.createFile("abcdef.png", 6)

    directory.children = [directory1, file1, file2]
    directory1.children = [file3]

    nameFilter = NameFilter("abcdef")
    extensionFilter = ExtensionFilter("png")

    andFilter = AndFilter()
    andFilter.addFilter(nameFilter)
    andFilter.addFilter(extensionFilter)

    result = fileSearchEngine.getFilesFromDirectory(directory, andFilter)
    
    print("\nFiles Found matching filters:")
    for file in result:
        print(f"- {file.name}")
