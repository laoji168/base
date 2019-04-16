package main

import (
    "fmt"
    "os"
)

func main() {
   //fmt.Println(util.MD5_MUI("laoji", "a"))
   //fmt.Println(util.String2MD5("laojia"))

    //u := util.UUID{
    //    'a','b','c','d',
    //    'e','f','g','h',
    //    'i','j','k','l',
    //    'm','n','o','p',
    //}
    //s := "abcabcabacbacbacbcbacbabcabcbacb"
    //b := []byte(s)
    //u := util.UUID{}
    //    for i,v := range b {
    //    if i < 16 {
    //        u[i] = v
    //    }
    //}
    //u, _ := util.FromStr(s)
    //fmt.Println(u)
    //fmt.Println(u.Hex())
    //fmt.Println(util.Rand())
    //var buf bytes.Buffer
    //logger := log.New(&buf, "logger:", log.LstdFlags)
    //logger.Print("Hello, log file!")
    //fmt.Println(&buf)
    //fmt.Println(logger.Flags())
    //fmt.Println(logger.Prefix())
    //fmt.Println(log.Prefix())
    //log.Println("hhahahha")

    //var b = []byte("Hello, good bye, etc!")
    //b = bytes.TrimSuffix(b, []byte("goodbye, etc!"))
    //b = bytes.TrimSuffix(b, []byte("gopher"))
    //b = append(b, bytes.TrimSuffix([]byte("world!"), []byte("d!"))...)
    //os.Stdout.Write(b)
    //fmt.Println()
    //for _, a := range bytes.SplitAfter(b, []byte{'o'}){
    //    os.Stdout.Write(a)
    //    fmt.Println()
    //}
    fmt.Println(os.Getwd())
}
