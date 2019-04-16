package main

import "fmt"
func main() {
    var a *[10]int
    malloc(a,[10]int)
    x:=78
    for i:=0;i<3;i++{
        (*a)[6]=i
        if (((*a)[6])==1) {
                x=2
        } else {
                print x,"\n"
        }
    }
    print x
}
