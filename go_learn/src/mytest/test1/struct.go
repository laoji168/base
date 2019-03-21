package main

import "fmt"

type Rect struct {
    x, y float64
    width, height float64
}

func (r *Rect) Area() float64 {
    return r.width * r.height
}

func init() {
    rect1 := new(Rect)
    rect2 := &Rect{}
    rect3 := &Rect{0,0,100,200}
    rect4 := &Rect{width:100, height:200}

    ShowRect(rect1)
    ShowRect(rect2)
    ShowRect(rect3)
    ShowRect(rect4)
}

func NewRect(x, y, width, height float64) *Rect {
    return &Rect{x, y, width, height}
}

func ShowRect(rect *Rect) {
    fmt.Println(rect.x, rect.y, rect.width, rect.height)
}

func main() {
    //Init()
    var rect *Rect  = NewRect(1.0, 2.0, 3.0, 4.0)
    ShowRect(rect)
    fmt.Println("area = ", rect.Area())
}
