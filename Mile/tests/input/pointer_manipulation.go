package main
var x int=100
func main() {
    var p *int
    p=&x
    *p=1000
    print *(&x)
}
