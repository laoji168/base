package main

import "fmt"

type Integer int

func (a Integer) Less(b Integer) bool {
    return a < b
}

func (a *Integer) add(b Integer) {
    *a += b
}

func main() {
    var a Integer = 1
    if a.Less(2) {
        fmt.Println(a, "less 2")
    }

    var b Integer =2
    a.add(b)
    fmt.Println("a = ", a)
}