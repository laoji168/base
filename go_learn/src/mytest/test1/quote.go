package main

import "fmt"

func testValue(){
    fmt.Println("for value")
    var a = [3]int {1, 2, 3}
    var b = a
    b[1]++
    fmt.Println("a = ",a, "\nb = ", b)
}

func testReference() {
    fmt.Println("for reference")
    var a = [3]int {1, 2, 3}
    var b = &a
    b[1]++
    fmt.Println("a = ",a, "\nb = ", *b)
}

func main() {
    testValue()
    testReference()
}
