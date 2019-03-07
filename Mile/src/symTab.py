class node:
    def __init__(self):
        self.idList=[]
        self.code=[]
        self.type=[]

class symbolTable:
    def __init__(self):
        self.table={}
        self.parent=None
        self.typeList=['int','float','string','rune','bool']

    def search(self,ident):
        return (self.table.get(ident))

    def insert(self,ident,attribute):
        if(not self.search(ident)):
    	    (self.table)[ident]={}
    	    self.table[ident]["type"]=attribute

    def updateList(self,ident,key,value):
        if(self.search(ident)):
            (self.table)[ident][key]=value

    def assignParent(self, parent):
        self.parent=parent
