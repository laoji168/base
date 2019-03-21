package main

import (
    "fmt"
    "strconv"
)

func getValue(n int) (float32, string) {
    var x float32 = float32(n)
    var str string = strconv.Itoa(n)
    return x, str
}

func main() {
    var n int = 10
    x, str := getValue(n)

    fmt.Printf("x=%f\nstr=%s\n", x, str)
}