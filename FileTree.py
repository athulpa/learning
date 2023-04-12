
import os

def getFileTree(rootPath="."):
    return {i:(getFileTree(os.path.join(rootPath,i)) if os.path.isdir(os.path.join(rootPath,i)) else {}) for i in os.listdir(rootPath)}

def printFileTree(dt, ilvl = 0):
    for i in dt.keys():
        print('\t'*ilvl, i)
        if(dt[i] is not None):
            printFileTree(dt[i], ilvl+1)
        
class FileTree:
    def __init__(self, arg=None, **kwargs):
        if(arg is None):        
            self._map = {}
            return
        if(type(arg) is dict):                    # convert dict to a FileTree
            if('argCheck' in kwargs.keys() and kwargs['argCheck'] is False):
                self._map = arg
            else:
                pass
        elif(type(arg) == type(self)):            # copy con'r
            pass
        elif(type(arg) is str):
            rootPath = arg
            try:
                flist = os.listdir(rootPath)
            except PermissionError:
                self._map = {}
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
        return (self._map == other._map)
    
    def __bool__(self):
        return bool(self._map)
    
    ### Printing Functions
    def toString(self, indentLvl=0, indentString='\t'):
        retString = ''
        for i in self._map.keys():
            retString += indentString*indentLvl + str(i) + '\n'
            if(self._map[i] is not None):
                retString += self._map[i].toString(indentLvl+1,indentString)    
        return retString

    def toString2(self, preIndent='', indentString=' '*3, lineCharIdx=0, lineChars=['\\','/']):
        retString = ''
        for i in self._map.keys():
            retString += preIndent + str(i) + '\n'
            if(self._map[i] is not None):
                nextIndent = preIndent + indentString + lineChars[lineCharIdx] + indentString
                lineCharIdx = (lineCharIdx + 1) % len(lineChars)
                retString += self._map[i].toString2(nextIndent, indentString, 0, lineChars)
        return retString
    
    def show(self, mode=None, **kwargs):
        ret = 'Not Implemented'
        if(mode==2):
            ret = self.toString2(**kwargs)
        else:
            ret = self.toString(**kwargs)
        print(ret)
        
    def __repr__(self):
        return 'keys(' + str(list(self._map.keys())) + ')'
    
    def __str__(self):
        return self.toString(0,'\t')
    
    def __sub__(self,other):
        if(type(other) != type(self)):
            raise NotImplementedError()
        
        d = {}
        for i in self.keys():
            #print("Checking", i)
            #input()
            if not(i in other.keys()):
                d[i] = self._map[i]
            else:
                if(self.isDir(i)):
                    
                    if(other.isFile(i)):
                        d[i] = self._map[i]
                    else:
                        #print("calling {0:} - {0:}".format(i))
                        #input()
                        diff = self._map[i] - other[i]
                        if(diff):
                            d[i] = diff
                else:
                    if(other.isDir(i)):
                        d[i] = self._map[i]                   
        
        return FileTree(d, argCheck=False)
        
        