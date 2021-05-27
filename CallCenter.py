"""
Call center -> Chain of responsiblities
"""
class Call:
    def __init__(self):
        self.rank = 0
    
    def disconnect(self):
        return "disconnect"
    
    def reply(self):
        return "reply"
    """
    caller, Employee handling the call getters and setters for rank
    """
    
"""
Employee is a super class for the Director, Manager, and Respondent classes. It is
implemented as an abstract class since there should be no reason to instantiate an
Employee type directly.
"""
class Employee:
    def __init__(self,rank = 0):
        self.callHandler = CallHandler()
        self.rank = 0
        self.free = True
    
    def receiveCall(self,call):
        self.free = False
        
    def callHandled(self,call):
        call.disconnect()
        free = True
        self.callHandler.nextCall()
    
    def callNotHandled(self,call):
        call.rank = self.rank+1
        callHandler.dispatchCall(Call)
        self.free = True
        callHandler.nextCall()
        
class Fresher(Employee):
    def __init__(self):
        Employee.__init__(self,0)

class TechLead(Employee):
    def __init__(self):
        Employee.__init__(self,1)

class ProductManager(Employee):
    def __init__(self):
        Employee.__init__(self,2)
 
"""
CallHandler is implemented as a singleton class. It represents the body of the program,
and all calls are funneled first through it.
"""
class CallHandler:
    def __init__(self):
        self.levels = 3
        self.numOfFreshers = 5
        self.employeeLevel = []
        self.callQueue = []
        for i in range(3):
            self.queue = collections.deque()
            self.callQueue.append(self.queue)
        self.freshers = []
        
        for i in range(self.numOfFreshers):
            fresher = Fresher()
            self.freshers.append(fresher)
        self.employeeLevel.append(self.freshers)
        
        #Add tech lead and productmanager
        
        self.employeeLevel.append(self.TL)
        self.employeeLevel.append(self.PM)
        
        
    def getCallHandler(self,call):
        for i in range(call.rank,self.levels-1):
            for emp in self.employeeLevel:
                for employee in emp:
                    if employee.free:
                        return employee
        return None
        
    def dispatchCall(self,call):
        employee = self.getCallHandler(call)
        if emp:
            emp.receiveCall(call)
        else:
            call.reply()
            self.callQueue[call.rank].append(call)
            
    def nextCall(self,emp):
        for i in range(emp.rank,-1,-1):
            q = self.callQueue[i]
            call = q.popleft()
            if call != None:
                emp.receiveCall(call)
                return
