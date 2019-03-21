package main

import (
    "fmt"
    "time"
)

func readThread(ch chan int)  {
    fmt.Println("read for reading...")
    for i := range ch {
        fmt.Println("get i:", i)
        if 20 == i {
            break
        }
        time.Sleep(1e8)
    }
    fmt.Println("read over...")
}

func main() {
    ch := make(chan int, 1024)
    go readThread(ch)
    time.Sleep(1e9 * 2)
    for i := 1; i <= 20; i++ {
        ch <- i
    }
    fmt.Println("waitting for reading...")
    time.Sleep(1e9 * 3)
    fmt.Println("over...")
}

//根据运行结果进行分析：
//
//　　1）先运行的readThread读线程，读线程已经做好了读的准备，但此时channel中还没有数据，所以阻塞了。等待读动作。
//
//　　2）主线程中，一次性向channel中写入大量数据，由于有缓冲机制，所以可以一次性的写入多个数据而不会阻塞。当主线程写完了数据，就开始等待读线程的读动作结束。
//
//　　3）channel中开始有数据，读线程开始读数据，每0.1秒钟读取一个数据，一共读取20次。读取结束了，打印read over。
//
//　　4）主线程等待的时间到了，返回，退出
