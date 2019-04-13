package main
import "fmt"
type ll struct {
	a    int
	next struct *ll
}
func main() {
    var find int
    scan find 

	var a1 ll
	var a2 ll
	var a3 ll
	var a4 ll
    var end ll 
	a1.a = 1
	a2.a = 2
	a3.a = 3
	a4.a = 4
	a1.next = &a2
	a2.next = &a3
	a3.next = &a4
	a4.next = &end
    var head *ll
    head = &a1
	found := False
	for {
		if head == &end {
			break
		}
		if ((*head).a == find) {
			found = True
			break
		}
		head = (*head).next
	}
	if found {
		print "Found\n"
	} else {
		print "Not found\n"
	}
}
