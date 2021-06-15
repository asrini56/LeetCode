from heapq import *
from collections import defaultdict, deque
class Twitter:

    # Each user has a separate min heap
    # if size of heap is lesser than 10 keep pushing tweets and when it's full, poppush
    # use a defaultdict to associate user id's to their heaps
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.following = defaultdict(set)
        self.user_tweets = defaultdict(deque)
        self.post = 0

    def postTweet(self, userId, tweetId):
        """
        Compose a new tweet.
        """
        self.post += 1
        tweets = self.user_tweets[userId]
        tweets.append(((self.post), tweetId))
        if len(tweets) > 10:
            tweets.popleft()
        

    def getNewsFeed(self, userId):
        """
        Retrieve the 10 most recent tweet ids in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user herself. Tweets must be ordered from most recent to least recent.
        """
        h = []
        u = self.user_tweets[userId]
        h.extend(u)
        heapify(h)
        for user in self.following[userId]:
            tweets = self.user_tweets[user]
            for x in range(len(tweets) - 1, -1, -1):
                if len(h) < 10:
                    heappush(h, tweets[x])
                else:
                    if h[0][0] < tweets[x][0]:
                        heappushpop(h, tweets[x])
                    else:
                        break
        return [heappop(h)[1] for x in range(len(h))][::-1]

    def follow(self, followerId, followeeId):
        """
        Follower follows a followee. If the operation is invalid, it should be a no-op.
        """
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        """
        Follower unfollows a followee. If the operation is invalid, it should be a no-op.
        """
        if followerId != followeeId:
                self.following[followerId].discard(followeeId)
