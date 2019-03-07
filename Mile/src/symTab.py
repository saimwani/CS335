class symbolTable

	def __init__(self):
		self.table={}
		self.parent=None

	def search(self,ident):
		return (ident in self.table)

	def insert(self,ident,attributes):
		if(not search(self,ident)):
			self.table[ident]={}
			self.table[ident]['type']=attributes

	def update(self,ident,key,value):
		if(search(self,ident)):
			self.table[ident][key]=value