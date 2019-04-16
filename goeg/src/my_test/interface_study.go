package main

import (
    "fmt"
    "strconv"
)

type I interface {
    HH(n int)
}

type M struct {
    name string
    I
}

type m int

func (m1 m) HH(n int) {
    fmt.Println(strconv.Itoa(n+int(m1)))
}

func main() {
    var a M
    var b m = 100
    a.name = "laoji"
    a.I = b
    fmt.Println(a.name, a.I)
    a.I.HH(2)

}
