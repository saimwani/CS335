with open("code.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]
codeLines=[]
j=0
for i in content:
    codeLines.append([])
    for x in i.split():
        codeLines[j].append(x)
    j+=1
flag=0
globalCode=[]
index=0
for i in range(0, len(codeLines)):
    if((len(codeLines[i])==2 and codeLines[i][1]==":") and (flag==0)):
        indexFirst=i
        flag=1
    elif(codeLines[i][0]=="main"):
        indexMain=i
        break

codeLines=codeLines[indexFirst:indexMain+1]+codeLines[0:indexFirst]+codeLines[indexMain+1:]

ring=""
f=open('codeFixed.txt', 'wr')
for code in codeLines:
    for x in range (0, len(code)):
        if(x==len(code)-1):
            ring=ring+code[x]
            print(ring +"\n")
            break
        ring=ring+code[x]+" "

    f.write(ring)
    ring=""
    f.write("\n")
f.close()



#for code in codeLines:
#    if (len(code) == 2
