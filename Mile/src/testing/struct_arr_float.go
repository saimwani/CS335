package main 
type arr struct{
    a [10]float
}
func main(){
    var temp arr
    var index float=1.0
    for i:=0;i<10;i++ {
        (temp.a)[i]=3.31*index 
        index+=1.0
        print (temp.a)[i]," ",index,"\n"
    }
}
