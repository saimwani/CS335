package main
func main(){
    var a [26]rune
    a[0]='a'
    i:=1
    for i<26 {
        a[i]=a[i-1]+'b'-'a'
        i++
    }
    for j:=0;j<26;j++{
        print a[j]," "
    }
    print "\n"
}
