# 并发编程

## 常用包

sync sync/atomic

## 关键概念

- 主goroutine（即main函数）退出后，其他的工作goroutine也会自动退出，若要完成其他工作，要保证主goroutine最后退出
- 死锁：
  1. 所有工作已完成，但主goroutine和工作goroutine还存活，通常由于主goroutine无法获得工作goroutine的完成状态
  2. 多个工作goroutine或线程同时锁定了受保护资源，且尝试获取时
  3. 常见作法：让主goroutine在一个done通道上等待，根据接收的信息判断工作是否完成
- 通道默认是双向，常用单向，会提供额外的编译期检查。本质上，通道传输布尔、整型、float64和字符串都是安全的，都是通过复制传送，而字符串也不允许修改。但当涉及指针和引用时，要保证任何时候只有一个goroutine访问，除非特别声明该指针安全，值不会改变。接口传递涉及到是否只读
- 并发使用：最简单的一种方式，一个goroutine来准备工作，另一个goroutine执行处理，主goroutine和通道安排一切事情

```go
//创建无缓冲区通道， 传递自定义Job类型的值和bool值
jobs := make(chan Job)
done := make(chan bool, len(jobList)) //有缓冲
//创建生产goroutine
go func() {
    for _, job := range jobList {
        jobs <- job  //阻塞， 等待接收，接收一个发送一个，发送完所有任务后，关闭通道，接收工作的goroutine便知道没其他工作了
    }
    close(jobs)
}()
//创建消费goroutine
go func() {
    for job := range jobs {	//等待发送数据
        fmt.Println(job)	//完成一项工作
        done <- true
    }
}
//主goroutine
for i:=0; i<len(jobList); i++ {
    <-done	//阻塞， 等待接收
}
```



