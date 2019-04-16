package main
var a int=3
func main(){
    var a0 *****int 
    var a1 ****int
    var a2 ***int
    var a3 **int
    var a4 *int
    a4=&a
    a3=&a4
    a2=&a3
    a1=&a2 
    a0=&a1

    *****a0=4
    print a,"\n"
}
