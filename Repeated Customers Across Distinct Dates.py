import collections
def findCustomer(records):
    date_map = collections.defaultdict(set)
    seen = set()
    
    for id,date in records:
        if date in date_map[id]:
            continue
        date_map[id].add(date)
        
        if len(date_map[id]) > 1:
            if id not in seen:
                seen.add(id)
    print(seen)
    return len(seen)

records = [["alice","Jan1"], ["bob", "Jan1"], ["alice", "Jan1"],["alice", "Jan2"],["carol", "Jan3"], ["bob","Jan2"]]

res = findCustomer(records)
print(res)
