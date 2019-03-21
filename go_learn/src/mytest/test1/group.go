package main

import "fmt"

type Base struct {
    Name string
}

func (base *Base) Foo()  {
    fmt.Println("Base Foo:", base.Name)
}

func (base *Base) Bar() {
    fmt.Println("Base Bar:", base.Name)
}

type Foo struct {
    Base
    a int
}

func (foo *Foo) Bar() {
    foo.Base.Bar()
    fmt.Println("\tFoo Bar:", foo.Name)
}

func main() {
    var str string = "hello world!!"
    base := &Base{str}
    base.Foo()

    str = "Ni Hao"
    foo := &Foo{Base{str}, 0}
    foo.Bar()
    foo.Foo()
}