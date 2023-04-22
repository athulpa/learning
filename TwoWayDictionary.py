
class TwoWayDict:
    def __init__(self, fromDict=None):
        self.l2r = dict()
        self.r2l = dict()
        
        if(fromDict is not None):
            for k in fromDict.keys():
                self.addPair(newLeft = k, newRight = fromDict[k])
                
        
    def containsLeftValue(self, val):
        return (val in self.l2r.keys())
    
    def containsRightValue(self, val):
        return (val in self.r2l.keys())
    
    
    def addPair(self, newLeft, newRight):
        oldRight = (self.l2r[newLeft]) if(newLeft in self.l2r.keys()) else None
        oldLeft  = (self.r2l[newRight]) if(newRight in self.r2l.keys()) else None
        
        self.l2r[newLeft] = newRight
        try:
            self.r2l[newRight] = newLeft
        except BaseException as BE:
            self.l2r[newLeft] = oldRight
            raise BE
        else:
            if (not(oldRight is None)) and (not(oldRight == newRight)):
                del self.r2l[oldRight]
            if (not(oldLeft is None)) and (not(oldLeft == newLeft)):
                del self.l2r[oldLeft]
        
            
            
    def getRightValue(self, leftKey):
        if(leftKey in self.l2r):
            return self.l2r[leftKey]
        else:
            raise KeyError("Couldn't find a corresponding right value for '{}'".format(leftKey))
        
    def getLeftValue(self, rightKey):
        if(rightKey in self.r2l):
            return self.r2l[rightKey]
        else:
            raise KeyError("Couldn't find a corresponding left value for '{}'".format(rightKey))
            
            
    def removeLeftValue(self, leftKey):
        if(leftKey in self.l2r.keys()):
            rightKey = self.l2r[leftKey]
            del self.l2r[leftKey]
            del self.r2l[rightKey]
        else:
            raise KeyError("No left value in the dict matches the given value: {}".format(leftKey))
            
    def removeRightValue(self, rightKey):
        if(rightKey in self.r2l.keys()):
            leftKey = self.r2l[rightKey]
            del self.r2l[rightKey]
            del self.l2r[leftKey]
        else:
            raise KeyError("No right value in the dict matches the given value: {}".format(rightKey))

    
    def copy(self):
        return TwoWayDict(fromDict = self.l2r)

    def __getattr__(self, name):
        if(name=='L'):
            return  _LeftInterface(self)
        elif(name=='R'):
            return _RightInterface(self)
        else:
            raise AttributeError("'TwoWayDict' object has no attribute '{}'".format(name))

    def __bool__(self):
        return (bool(self.l2r) or bool(self.r2l))
    
##################################################
##     INTERFACES FOR USING BUILT-IN SYNTAX
##################################################

class _LeftInterface:
    def __init__(self, twoWayDict):
        self.twoWayDict = twoWayDict
        
    def asDict(self, copy=True):
        if(copy is False):
            return self.twoWayDict.l2r
        else:
            return {i:self.twoWayDict.l2r[i] for i in self.twoWayDict.l2r}
        
    def __getitem__(self, key):
        return self.twoWayDict.getRightValue(leftKey = key)
    
    def __setitem__(self, key, value):
        self.twoWayDict.addPair(newLeft=key, newRight=value)
    
    def __delitem__(self, key):
        self.twoWayDict.removeLeftValue(leftKey = key)
    
    def __str__(self):
        return str(self.twoWayDict.l2r)
    
    def __repr__(self):
        return str(self)
    
    def __contains__(self, val):
        return self.twoWayDict.containsLeftValue(val)

    def __len__(self):
        return len(self.twoWayDict.l2r)
    
    def __bool__(self):
        return bool(self.twoWayDict)
    
    
class _RightInterface:
    def __init__(self, twoWayDict):
        self.twoWayDict = twoWayDict
        
    def asDict(self, copy=True):
        if(copy is False):
            return self.twoWayDict.r2l
        else:
            return {i:self.twoWayDict.r2l[i] for i in self.twoWayDict.r2l}
        
    def __getitem__(self, key):
        return self.twoWayDict.getLeftValue(rightKey = key)
    
    def __setitem__(self, key, value):
        self.twoWayDict.addPair(newRight=key, newLeft=value)
    
    def __delitem__(self, key):
        self.twoWayDict.removeRightValue(rightKey = key)
    
    def __str__(self):
        return str(self.twoWayDict.r2l)
    
    def __repr__(self):
        return str(self)
    
    def __contains__(self, val):
        return self.twoWayDict.containsRightValue(val)

    def __len__(self):
        return len(self.twoWayDict.r2l)
    
    def __bool__(self):
        return bool(self.twoWayDict)