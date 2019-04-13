package main

import "fmt"

func mutate(k *[10]int) {
	(*k)[2] = 2
}

func main() {
	var a [10]int
	var b *[10]int
	b = &a
	a[2] = 1
	print a[2],"\n"
	mutate(b)
    // a[2]=3
	print a[2],"\n"
}
