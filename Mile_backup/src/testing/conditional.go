package main

import "fmt"
var a int
func main() {
    scan a
	if a <= 10 {
		if a <= 5 {
			print "A is <= 5\n"
		} else {
			print "A is >= 5\n"
		}
	} else {
		print "A is non <= 10\n"
	}
}
