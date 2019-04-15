package main

import "fmt"

var a int
var b [45]int

func main() {
	a = 10
	print a,"\n"
	for i := 0; i < 45; i++ {
		b[i] = i + 67
	}
	for i := 0; i < 45; i++ {
		print b[i],"\n"
	}
}
