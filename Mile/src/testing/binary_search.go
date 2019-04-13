package main

import "fmt"

func main() {
	n := 5
	var a [5]int
	for i := 0; i < n; i++ {
		scan a[i]
	}

	start := 0
	end := n - 1
	key := 8

    for start <= end {
        print start," ",end,"\n"
		m := start + (end-start)/2
        print m,"\n"
		if a[m] == key {
			print "found at index ",m
            return
		}

		if a[m] < key {
			start = m + 1
		} else {
			end = m - 1
		}
	}
    print "not found"
}
