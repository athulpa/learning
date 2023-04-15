
import os
import json

class FileTree:
    def __init__(self, arg=None, **kwargs):
        self._map = {}
        if(arg is None):        
            return
        if(type(arg) is dict):                    # convert dict to a FileTree
            if('argCheck' in kwargs.keys() and kwargs['argCheck'] is False):
                ### Only works if 'argCheck' is set to False
                ### Allows the dev to set the _map attribute directly
                self._map = arg
        elif(type(arg) is str):
            rootPath = arg
            try:
                flist = os.listdir(rootPath)
            except PermissionError:
                return
            else:
                self._map = {i:None for i in flist}
                for i in flist:
                    fullPath = os.path.join(rootPath, i)
                    if(os.path.isdir(fullPath)):
                        self._map[i] = FileTree(fullPath)
            
        
    
    def isFile(self,key):
        return (self._map[key] is None)
    
    def isDir(self,key):
        return not(self.isFile(key))
    
    def isEmpty(self):
        return not bool(self._map)
    
    
    
    ####################
    ## TYPE CONVERSION
    ####################
    
    def asDict(self):
        return { (k):(self._map[k].asDict() if(self.isDir(k)) else None)
                  for k in self._map.keys()}
    @staticmethod
    def fromDict(treeDict):
        return FileTree(  
                         {(k):(None if(treeDict[k] is None) else FileTree.fromDict(treeDict[k]))
                                   for k in treeDict.keys()}
                         , argCheck=False
                    )
        
    
    
    ######################
    ## PRINTING METHODS
    ######################
    
    # Only top-level items (doesn't print the tree)
    def displayMethod0(self, preString='', separator='\n', endString='', folderMarker='', fileMarker=''):
        ret = preString
        for k in self._map.keys():
            ret += separator
            ret += (folderMarker) if (self.isDir(k)) else (fileMarker)
            ret += str(k)
        return ret
    
    # Show full tree with custom options
    def displayMethod1(self, indentLvl=0, indentString='\t'):
        retString = ''
        for i in self._map.keys():
            retString += indentString*indentLvl + str(i) + '\n'
            if(self._map[i] is not None):
                retString += self._map[i].displayMethod1(indentLvl+1,indentString)    
        return retString

    # Show full tree with custom options
    def displayMethod2(self, preIndent='', indentString=' '*3, lineCharIdx=0, lineChars=['\\','/']):
        retString = ''
        for i in self._map.keys():
            retString += preIndent + str(i) + '\n'
            if(self._map[i] is not None):
                nextIndent = preIndent + indentString + lineChars[lineCharIdx] + indentString
                lineCharIdx = (lineCharIdx + 1) % len(lineChars)
                retString += self._map[i].displayMethod2(nextIndent, indentString, 0, lineChars)
        return retString
    
    # Common interface to call a select printing function
    def show(self, mode=None, **kwargs):
        ret = 'Not Implemented'
        if(mode==2):
            ret = self.displayMethod2(**kwargs)
        elif(mode==1):
            ret = self.displayMethod1(**kwargs)
        elif(mode==0):
            ret = self.displayMethod0(**kwargs)
        print(ret)
    
    
    
    #######################
    #  LOAD/SAVE METHODS
    #######################

    def save(self, fileName):
        d = self.asDict()
        with open(fileName, "w") as outFile:
            json.dump(d, outFile)
    
    @staticmethod
    def load(fileName):
        with open(fileName, "r") as inFile:
            d = json.load(inFile)
        return FileTree.fromDict(d)
    
    
    
    ####################
    #  COUNTING ALGO
    ####################
    
    def numItems(self):
        total = len(self.keys())
        for k in self.keys():
            if(self.isDir(k)):
                total += self._map[k].numItems()
        return total
        
    
    
    ########################
    #  SET DIFFERENCE ALGO
    ########################
    
    def setDifference(self,other):
        if(type(other) != type(self)):
            raise NotImplementedError()

        d = {}
        for i in self.keys():
            if not(i in other.keys()):
                d[i] = self._map[i]
            else:
                if(self.isDir(i)):

                    if(other.isFile(i)):
                        d[i] = self._map[i]
                    else:
                        diff = self._map[i].setDifference(other[i])
                        if(diff):
                            d[i] = diff
                else:
                    if(other.isDir(i)):
                        d[i] = self._map[i]                   

        return FileTree(d, argCheck=False)
    


    ####################
    #  EQUALITY ALGOS
    ####################
    
    # Shallow Equality
    def isEqual_Shallow(self, other):
        if(len(self) != len(other)):
            return False
        for i in self.keys():
            if(i not in other.keys() or self.isDir(i)!=other.isDir(i)):
                return False
            
    # Deep Equality
    def isEqual_Deep(self, other):
        return (self._map == other._map)
    
    
    
    ########################
    #  PYTHONIC INTERFACE
    ########################
    
    def keys(self):
        return list(self._map.keys())
    
    def __len__(self):
        return len(self._map)
    
    def __dir__(self):
        return self._map.keys()
    
    def __getattr__(self, name):
        if name!='_map':
            return self._map[name]
    
    def __getitem__(self, key):
        return self._map[key]
    
    def __eq__(self, other):
        if(type(other)!=type(self)):
            return False
        return self.isEqual_Deep(other)
    
    def __bool__(self):
        return not self.isEmpty()
    
    def __sub__(self,other):
        return self.setDifference(other)
    
    def __str__(self):
        return self.displayMethod1(0,'\t')
    
    def __repr__(self):
        if(self.isEmpty()):
            return "Nothing to see here!"
        return self.displayMethod0(preString="TOP-LEVEL ITEMS :\n", folderMarker='(dir) ')
    
        


####################
#  OUTER FUNCTIONS
####################

def getFileTree(rootPath="."):
    return {i:(getFileTree(os.path.join(rootPath,i)) if os.path.isdir(os.path.join(rootPath,i)) else {}) for i in os.listdir(rootPath)}

def printFileTree(dt, ilvl = 0):
    for i in dt.keys():
        print('\t'*ilvl, i)
        if(dt[i] is not None):
            printFileTree(dt[i], ilvl+1)
                