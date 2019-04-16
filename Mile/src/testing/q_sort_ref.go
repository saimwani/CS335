package main

import "fmt"


func partition(A *[30]int,p int, r int) (int) {
	x := (*A)[p]
	i := p - 1
	j := r + 1

	for {
		j--
		kk := (*A)[j]
		for kk < x {
			j--
			kk = (*A)[j]
		}
		i++
		for (*A)[i] > x {
			i++
		}
		if i < j {
			tmp := (*A)[i]
			(*A)[i] = (*A)[j]
			(*A)[j] = tmp
		} else {
			return j
		}
	}
	return -1
}
func qsort(A *[30]int,p int, r int) {
	if p < r {
		q := partition(A,p, r)
		qsort(A,p, q)
		qsort(A,q+1, r)
	}
}

func main() {
    var A [30]int
	for i := 0; i < 30; i++ {
		n := 0
		scan A[i]
	}

	for i := 0; i < 3; i++ {
		for j := 0; j < 10; j++ {
			print A[10*i+j]," "
		}
		print "\n"
	}

	print "\n"
	qsort(&A,0, 29)

	for i := 0; i < 3; i++ {
		for j := 0; j < 10; j++ {
			print A[10*i+j]," "
		}
		print "\n"
	}
}

