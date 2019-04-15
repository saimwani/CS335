package main

import "fmt"

func fibo_iter(n int) {
	a := 0
	b := 1
	for i := 0; i < n; i++ {
		print a,"\n"
		tmp := a + b
		a = b
		b = tmp
	}
}

func main() {
	a := 0
	scan a
	fibo_iter(a)
}
