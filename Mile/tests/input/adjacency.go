package main

import "fmt"

type kk struct {
	a int
	b struct *kk
}

func main() {
	var str [10]*kk

    
    var n int
    scan n
	for i := 0; i < 10; i++ {
		
        malloc(str[i],kk)
		var ptr *kk
        ptr = str[i]
		for j := 0; j < n; j++ {
			(*ptr).a = 10 + (i*10) + j
			malloc((*ptr).b,kk)
			ptr = (*ptr).b
		}
	}

	for i := 0; i < 10; i++ {
		var ptr *kk
        ptr = str[i]
		for j := 0; j < n; j++ {
			print (*ptr).a,"\n"
			ptr = (*ptr).b
		}
	}
}
