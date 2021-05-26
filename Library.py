#Online Reader System -> Library
"""
User membership creation and extension.
• Searching the database of books.
• Reading a book.
• Only one active user at a time
• Only one active book by this user
"""

class User:
    def __init__(self):
        self.name = None
        self.userID = None
    
    # Getters and Setters for username and userID

class Book:
    """
    bookname,bookid Getters and Setters
    """

"""
Library, usermanager, display 
Library and usermanager -> composite patterns
"""

class Library:
    def __init__(self,books = {}):
        self.books = books
    def addbook(self,bookname,bookid):
        book = Book(bookname,bookid)
        self.books[bookid] = book
    def removebook(self,book,bookid):
        del self.books.[bookid]
    def findbook(self,book):
        #logic to find book

class UserManager:
    def __init__(self,v = {}):
        self.userList = v
    """
    Getters and Setters for userList
    """
    def addUser(self,username,userId):
        user = User(username,userID)
        self.userList[userID] = user
    def removeUser(self,userID,username):
        del self.userList[userID]

class Display:
    """
    displayActive user,book
    turn pages -> addpagenumber, refreshpage
    """

"""
The class OnlineReaderSystem represents the body of our program. We would
implement the class such that it stores information about all the books, deals with user
management, and refreshes the display, but that would make this class rather hefty.
Instead, we've chosen to tear off these components into Library, UserManager, and
Display classes.
"""

class OnlineReaderSystem:
    def __init__(self,UserManager,Library,Display,activeBook,activeUser):
        """
        assign
        """
    """
    Getters and Setters for all and get active book and User
    """
"""
Payment System -> abstract class with different payment methods implementing them
"""
