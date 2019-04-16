package main
//
//import (
//    "fmt"
//    "reflect"
//)

type X int
type Y int

type user struct {
    name string
    age int
}

type manager struct {
    user
    title string
}

type A int
type B struct {
    A
}

func (A) av() {}
func (*A) ap() {}
func (B) bv() {}
func (*B) bp() {}

func add(x, y int) int {
    return x + y
}

func main() {

    //var b B
    //t := reflect.TypeOf(&b)
    //s := []reflect.Type{t, t.Elem()}
    //for _, t := range s {
    //    fmt.Println(t, ":")
    //    println(t.NumMethod())
    //    for i := 0; i < t.NumMethod(); i++ {
    //        fmt.Println("  ", t.Method(i))
    //    }
    //}

    //var a X = 100
    //t := reflect.TypeOf(a)
    //fmt.Println(t.Name(), t.Kind())

    //var a, b X = 100, 200
    //var c Y = 300
    //ta, tb, tc := reflect.TypeOf(a), reflect.TypeOf(b), reflect.TypeOf(c)
    //fmt.Println(ta == tb, ta == tc)
    //fmt.Println(ta.Kind() == tc.Kind())

    //a := reflect.ArrayOf(10, reflect.TypeOf(byte(0)))
    //m := reflect.MapOf(reflect.TypeOf(""), reflect.TypeOf(0))
    //fmt.Println(a, m)

    //a := 100
    //tx, tp := reflect.TypeOf(a), reflect.TypeOf(&a)
    //fmt.Println(tx, tp, tx == tp)
    //fmt.Println(tx.Kind(), tp.Kind())
    //fmt.Println(tp.Elem())
    //fmt.Println(tx == tp.Elem())

    //fmt.Println(reflect.TypeOf(map[string]int{}).Elem())
    //fmt.Println(reflect.TypeOf([]int32{}).Elem())

    //var m manager
    //t := reflect.TypeOf(&m)
    //if t.Kind() == reflect.Ptr {
    //    t = t.Elem()
    //}
    //for i := 0; i < t.NumField(); i++ {
    //    f := t.Field(i)
    //    fmt.Println(f.Name, f.Type, f.Offset)
    //    //输出匿名字段结构
    //    if f.Anonymous {
    //        for x := 0; x < f.Type.NumField(); x++ {
    //            af := f.Type.Field(x)
    //            fmt.Println("  ", af.Name, af.Type)
    //        }
    //    }
    //}

    //var m manager
    //t := reflect.TypeOf(m)
    //fmt.Println(t)
    //name, _ := t.FieldByName("name")
    //fmt.Println(name.Name, name.Type)
    //age := t.FieldByIndex([]int{0, 1})
    //fmt.Println(age.Name, age.Type)


}



