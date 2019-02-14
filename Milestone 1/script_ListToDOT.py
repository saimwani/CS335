file1 = open("treeGen.txt","w")#write mode
#file1 = open(outputHtml,"a")
file1.write("digraph graphname {")
file1.write("\n")

counter=0
def writeGraph(someList):
    global counter
    local=counter
    counter+=1
    name=someList[0]
    if(len(someList) > 1):
        for innerList in someList[1:]:
            if(len(innerList) >0):
                file1.write(str(local))
                file1.write ("[label=\"")
                file1.write (name)
                file1.write ("\" ] ;")
                file1.write(str(counter))
                file1.write ("[label=\"")
                if ((innerList[0][0])=="\""):
                    innerList[0]=innerList[0][1:-1]
                file1.write (innerList[0])
                file1.write ("\" ] ;")
                file1.write(str(local) + "->" + str(counter) + ";")
                file1.write("\n")
                writeGraph(innerList)
alist=['SourceFile', ['main'], ['ImportDecl_curl', [], ['"fmt"']], ['TopLevelDecl_curl', ['TopLevelDecl_curl', [], ['TypeDecl', ['type'], ['TypeDef', ['Vertex'], ['StructType', ['struct'], ['FieldDecl_curl', ['FieldDecl_curl', [], ['FieldDecl', ['X'], ['int']]], ['FieldDecl', ['Y'], ['int']]]]]]], ['FunctionDecl', ['main'], ['Signature', ['Parameters', []], []], ['Statement_curl', ['Statement_curl', [], ['PrimaryExpr', ['PrimaryExpr', ['fmt'], ['.'], ['Println']], ['Arguments', ['CompositeLit', ['Vertex'], ['ElementList', ['1'], ['2']]]]]], ['ForStmt', ['for'], ['ForClause', ['ShortVarDecl', ['i'], [':='], ['0']], [';'], ['Expression', ['i'], ['<'], ['10']], [';'], ['IncDecStmt', ['i'], ['++']]], ['Statement_curl', [], ['Assignment', ['sum'], ['+='], ['i']]]]]]]]


writeGraph(alist)
file1.write("}")
file1.close()

