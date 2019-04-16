package main
type Vertex struct{
    x,y int
    c struct *Vertex 
}
func ran(a Vertex) (int,int){
    print (a.x)*(a.x),"\n"
    print (a.y)+(a.x),"\n"
    return (*(a.c)).x,(*(a.c)).y
    // return a.x,a.y
}
func main(){
    
    
    var a Vertex
    var b *Vertex
    a.x=1
    a.y=2
    malloc(b,Vertex)
    a.c=b
    (*b).x=100
    (*b).y=200
    e,f := ran(a)
    print e,"\n",f,"\n"
}

