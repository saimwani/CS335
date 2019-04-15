package main

func main(){
    var a,b int
    scan a
    scan b
    switch b {
        case a+3:
            print "Second integer is 3 greater than first integer","\n"
        case a+2:
            print "Second integer is 2 greater than first integer","\n"
        case a+1:
            print "Second integer is 1 greater than first integer","\n"
        case a:
            print "Second integer is equal to first integer","\n"
        default:
            print "The rest cases","\n"
    }
}

