package main

import (
    "fmt"
    "time"
)

func waitFor(ch chan int)  {
    fmt.Println(time.Now(), "writing...")
    time.Sleep(1e9)
    ch <- 10
    fmt.Println(time.Now(), "wrote...")
}

func main() {
    var a chan int = make(chan int)
    var b chan int = make(chan int)
    var ch chan int = make(chan int)

    go waitFor(ch)

    var r int = 0
    fmt.Println(time.Now(), "select ...")
    select {
    case x := <-a :
        fmt.Println(time.Now(), "read from a ...")
        r = x
    case x := <- b :
        fmt.Println(time.Now(), "read from b ...")
        r = x
    case x := <-ch:
        fmt.Println(time.Now(), "read from ch ...")
        r = x
    }

    fmt.Println(time.Now(), "select over ..., r=",r)
    time.Sleep(1e9)
    fmt.Println(time.Now(), "over...")
}

//1）主线程中的select开始运行，对select中的3个channel进行阻塞等待
//
//　　2）在线程（协程）waitFor中向ch写入数据
//
//　　3）select收到数据，进行读取
//
//　　4）主线程退出