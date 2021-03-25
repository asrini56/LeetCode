class UndergroundSystem:

    def __init__(self):
        self.ids = {}
        self.pair = Counter()
        self.freq = Counter()

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.ids[id] = (stationName,t)
        

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        name,time = self.ids.pop(id)
        self.pair[(name,stationName)]+= t-time
        self.freq[(name,stationName)]+=1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        return self.pair[(startStation,endStation)]/self.freq[(startStation,endStation)]


# Your UndergroundSystem object will be instantiated and called as such:
# obj = UndergroundSystem()
# obj.checkIn(id,stationName,t)
# obj.checkOut(id,stationName,t)
# param_3 = obj.getAverageTime(startStation,endStation)
