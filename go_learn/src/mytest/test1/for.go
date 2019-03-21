package main

import "fmt"

func main()  {

    for k:=0; k<5; k++ {
        JLoop:
            for j:=0; j<5; j++ {
                for i:=0; i<10; i++ {
                    if i > 5 {
                        break JLoop
                    }
                    fmt.Printf("%d", i)
                }
            }
            fmt.Println("k")
    }
    fmt.Println("Hello World!!")
    
}