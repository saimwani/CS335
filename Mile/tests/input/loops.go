package main

import "fmt"

func main() {
	i := 0
	for i=0; i < 10; i++ {
		for j := 0; j < 20; j += 1 {
			print i," ",j," "
		}
		print "\n"
	}
}
