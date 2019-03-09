class node:
    def __init__(self):
        self.idList=[]
        self.code=[]
        self.type=[]
        self.expTList=[]
        self.expList=[]
        self.info={}

class symbolTable:
    def __init__(self):
        self.table={}
        self.labels={}
        self.parent=None
        self.typeList=['int','float','string','rune','bool']

    def search(self,ident):
        return (self.table.get(ident))

    def insert(self,ident,attribute):
        if(not self.search(ident)):
    	    self.table[ident]={}
    	    self.table[ident]["type"]=attribute

    def updateList(self,ident,key,value):
        if(self.search(ident)):
            self.table[ident][key]=value

    def searchL(self,labelname):
        return self.labels.get(labelname)
    
    def insertL(self,labelname,attribute):
        if(not self.searchL(labelname)):
    	    self.labels[labelname]={}
    	    self.labels[labelname]["info"]=attribute

    def assignParent(self, parent):
        self.parent=parent
