class symbolTable:
    def __init__(self):
	self.table={}
	self.parent=None

	def search(self,ident):
		return (ident in self.table)

	def insert(self,ident,attribute):
		if(not self.search(ident)):
			(self.table)[ident]={}
			self.table[ident]["type"]=attribute

	def updateList(self,ident,key,value):
		if(self.search(ident)):
			(self.table)[ident][key]=value

    def assignParent(self, parent):
        self.parent=parent
