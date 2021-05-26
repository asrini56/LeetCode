"""
Now that we have that out of the way, we'll outline the basic system components.
• Jukebox
• CD
• Song
• Artist
• Playlist
• Display (displays details on the screen)
Now, let’s break this down further and think about the possible actions.
• Playlist creation (includes add, delete, and shuffle)
• CD selector
• Song selector
• Queuing up a song
• Get next song from playlist
A user also can be introduced:
• Adding
• Deleting
• Credit information
"""

#Music Jukebox
"""
User,CD,Song
"""
import collections
class User:
    def __init__(self):
        self.name = None
        self.userID = None
    
    # Getters and Setters for username and userID

class Song:
    """
    songname, artist name,id,length,CD
    """

class CD:
    """
    id,artist,songs
    """
"""
The Playlist manages the current and next songs to play. It is essentially a wrapper
class for a queue and offers some additional methods for convenience.
"""
class PlayList:
    def __init__(self,song,queue):
        self.song = song
        self.queue = queue #collections.deque()
        
    def queueUpSong(self,song):
        self.queue.append(song)
    
    def peekSong(self):
        return self.queue[0]
    
"""
Like a real CD player, the CDPlayer class supports storing just one CD at a time. The
CDs that are not in play are stored in the jukebox.
"""

class CDPlayer:
    def __init__(self,playList,cd):
        self.playList = playList
        self.cd = cd
    def playSong(self,song):
        #logic for play song
    """
    Getters and Setters for playList and cd {getPlaylist,getCd...}
    """
"""
UserManager
"""
class UserManager:
    def __init__(self,v = []):
        self.userList = v
    """
    Getters and Setters for userList
    """
    def addUser(self,user):
        self.userList.append(user)
    def removeUser(self,user):
        self.userList.remove(user)

"""
The Jukebox class represents the body of the problem. Many of the interactions
between the components of the system, or between the system and the user, are
channeled through here.
"""

class Jukebox:
    def __init__(self,user =None,playList = None,cds = set(),CDPlayer = None):
        self.user = user
        #...
    #Getters and Setters for parameters
    
    def getCurrentSong(self):
        #Logic

"""
Additional Payment class -> can be abstract class and payment methods such as coins or card
Inventory class for maintaining payment information
coin class etc
"""
    
