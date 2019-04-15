package main
func square(a [10]int){
    for i:=0;i<10;i++{
        print a[i]," "
    }
    print "\n"
}
func main(){
    var a [10]int
    for i:=0;i<10;i++ {
        a[i]=i*i
    }
    square(a)
}
