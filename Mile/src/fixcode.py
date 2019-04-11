import os
with open("mips.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]
j=0
codeLines=[]
for i in content:
    codeLines.append([])
    for x in i.split():
        codeLines[j].append(x)
    j+=1
f.close()

saveMsgs=[]


leng=len(codeLines)

for i in range(0, leng):
    if(i==len(codeLines)):
        break
    #print(i, leng, len(codeLines), "\n")
    if (codeLines[i][0][0:4]=="msg#"):
        saveMsgs.append(codeLines.pop(i))
        leng-=1
print saveMsgs



codeLines=[codeLines[0]]+saveMsgs+codeLines[1:]
#print codeLines

f=open('mips.txt', 'wr')
for x in codeLines:
	if(len(x)==1):
		if(x[0]=="syscall"):
			f.write("\t")
		f.write(x[0]+"\n")
	elif(x[0]==".globl"):
		f.write(x[0]+" "+x[1]+"\n")
	else:
		for index in range(0,len(x)):
			f.write("\t"+x[index]+" ")
		f.write("\n")

f.close()
