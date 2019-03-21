package main

import "fmt"

func switch_1(i int)  {
    switch i {
    case 0:
        fmt.Println("0 --:i = ", i)
    case 1:
        fmt.Println("1 --:i = ", i)
    case 2:
        fmt.Println("2 --:i = ", i)
        fallthrough
    case 3:
        fmt.Println("3 --:i = ", i)
    case 4 ,5 , 6:
        fmt.Println("4, 5, 6 --:i = ", i)
    default:
        fmt.Println("Default --:i = ", i)
    }
}

func switch_2(i int)  {
    switch  {
    case 0 <= i && i <= 3:
        fmt.Println("0-3 --:i = ", i)
    case 4 <= i && i <= 6:
        fmt.Println("4-6 --:i = ", i)
    case 7 <= i && i <= 9:
        fmt.Println("7-9 --:i = ", i)
    }
}

func main()  {
    for i:=0; i<=6;i++ {
        switch_1(i)
    }

    fmt.Println("------------------------")
    for j:=0; j<=6; j++ {
        switch_2(j)
    }

}