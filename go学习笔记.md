将两个(或更多)语句放在一行书写，它们 必须用分号 (’;’) 分隔。一般情况下，你不需要分号。

# init函数和main函数

Go里面有两个保留的函数：init函数（能够应用于所有的package）和main函数（只能应用于package main）。这两个函数在定义时不能有任何的参数和返回值。虽然一个package里面可以写任意多个init函数，但这无论是对于可读性还是以后的可维护性来说，我们都强烈建议用户在一个package中每个文件只写一个init函数。
Go程序会自动调用init()和main()，所以你不需要在任何地方调用这两个函数。每个package中的init函数都是可选的，但package main就必须包含一个main函数。
程序的初始化和执行都起始于main包。如果main包还导入了其它的包，那么就会在编译时将它们依次导入。有时一个包会被多个包同时导入，那么它只会被导入一次（例如很多包可能都会用到fmt包，但它只会被导入一次，因为没有必要导入多次）。当一个包被导入时，如果该包还导入了其它的包，那么会先将其它包导入进来，然后再对这些包中的包级常量和变量进行初始化，接着执行init函数（如果有的话），依次类推。等所有被导入的包都加载完毕了，就会开始对main包中的包级常量和变量进行初始化，然后执行main包中的init函数（如果存在的话），最后执行main函数。下图详细地解释了整个执行过程：



![1553061039286](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1553061039286.png)

# 类型

## 声明与赋值

**1、变量的类型在变量名的后面:**

```go
var a int
```

**2、声明和赋值（只在函数和方法内部）：**

```go
a := 15
```

**3、多 个 var 声明可以成组:**

```go
var (
	x int
    y bool
)
```

**4、相同类型的多个变量:**

```go
var x, y int
```

**5、平行赋值:**

```go
a, b = 20, 16
```

**一个特殊的变量名是 _(下划线)。任何赋给它的值都被丢弃。**

## 数值类型

int8，int16，int32，int64 和 byte，uint8，uint16，uint32， uint64。byte 是 uint8 的别名。
浮点类型的值有 float32 和 float64
这些类型全部都是独立的，并且混合用这些类型向变量赋值会引起编译器错误。
rune 是 int32 的别名。

**常量在编译时被创建，只能是数字、字符串或布尔值。**
**生成常量x**：

```go
const x = 42
```

**生成枚举值：**

```go
const (
    a= iota  // a == 0
    b= iota  // b == 1, “=iota”可以省略
)
```

## 字符串

字符串在 Go 中是 UTF-8 的由双引号(”)包裹的字符序列。如果你使用单引号(’)则 表示一个字符(UTF-8 编码)——这种在 Go 中不是 string。
一旦给变量赋值，字符串就不能修改了:在 Go 中字符串是不可变的。
Go 原生支持复数。它的变量类型是 complex128 (64 位虚数部分)。如果需要小一些 的，还有 complex64 – 32 位的虚数部分。复数写为 re + imi，re 是实数部分，im 是 虚数部分，而 i 是标记 ’i’ (√−1)。
错误的内建类型error，值为nil：
var e error

## 运算符

运算优先级：

*     /     %    <<    >>    &    &^    +    -    |    ^    
      ==    !=    <    <=    >     >=   <-    &&   ||

# 控制结构

**if** 接受初始化语句，通常用于设置一个(局部)变量。

```go
if err := Chmod(0664); err != nil { // nil 与 C 的 NULL 类似，大括号与if必须在同一行
    fmt.Printf(err) ← err 的作用域被限定在 if 内
    return err
}
```

用 **goto** 跳转到当前函数内定义的标签。
这是一个无限循环：

```go
func myfunc() { 
    i := 0
Here:       // 这行的第一个词，以冒号结束作为标签 
    println(i)
    I++
    goto Here   // 跳转
}
```

**for** 循环有三种形式，只有其中的一种使用分号。

for init; condition; post { }     和C的for一样
for condition { }                    和while一样
for { }                                死循环

Go 没有逗号表达式，而 ++ 和 -– 是语句而不是表达式.
利用 break 可以提前退出循环，continue 终止当前的循环。
J: for j:=0; j<5; j++ {
​    for i:=0; i<10; i++ {
​        if i>5 { 
​            break J     // 终止的是J循环，而不是i那个
​        }
​        println(i)
​    } 
}

**range 是个迭代器**，当被调用的时候，从它循环的内容中返回一个键值对。基于不同的内容，range 返回不同的东西。
当对 slice 或者 array 做循环时，range返回序号作为键，这个序号对应的内容作为值。
**switch** 非常灵活。表达式不必是常量或整数，执行的过程从上至下，直到找到匹配项，而如果 switch 没有表达式，它会匹配 true。switch不会匹配失败后自动向下尝试，但是可以使用 **fallthrough** 使其这样做。

# 内建函数

**无需引用任何包就可以使用它们**：
**close new panic complex delete make recover** 
**real len append print imag cap copy println**

# array

array 由 [n]<type> 定义，n 标示 array 的长度，而 <type> 标示希望存储的内容的类 型。对 array 的元素赋值或索引是由方括号完成的。有固定的大小，不能改变。

```go
var arr [10]int
arr[0] = 42
var a = new([10]int)
a := [3]int{1, 2, 3} // 复合声明
a := [...]int{1, 2, 3} // 简写，Go会自动统计元素的个数。
```

多维数组：

```go
a := [3][2]int { [2]int {1,2}, [2]int {3,4}, [2]int {5,6} }
a := [3][2]int { [...]int {1,2}, [...]int {3,4}, [...]int {5,6} }
a := [3][2]int { {1,2}, {3,4}, {5,6} }
```

# slice

slice 与 array 接近，但是在新的元素加入的时候可以增加长度。slice 总是指向底层的 一个 array。slice 是一个指向 array 的指针，这是其与 array 不同的地方;slice 是引用类型，这意味着当赋值某个 slice 到另外一个变量，两个引用会指向同一个 array。
slice 总 是与一个固定长度的 array 成对出现。给定一个 array 或者其他 slice，一个新 slice 通过 a[I:J] 的方式创建。
var array[m]int
slice := array[0:n]

创建一个保存有 10 个元素的 slice：
sl := make([]int, 10)

函数 append 向 slice s 追加零值或其他 x 值，并且返回追加后的新的、与 s 有相同类型的 slice。如果 s 没有足够的容量存储追加的值，append 分配一 个足够大的、新的 slice 来存放原有 slice 的元素和追加的值。因此，返回 的 slice 可能指向不同的底层 array。
s0 := []int {0, 0}
s1 := append(s0, 2) 0        // 追加一个元素，s1 == []int{0, 0, 2};
s2 := append(s1, 3, 5, 7)    // 追加多个元素，s2 == []int{0, 0, 2, 3, 5, 7}; 
s3 := append(s2, s0...)      // 追加一个 slice，s3 == []int{0, 0, 2, 3, 5, 7, 0, 0}。注意这三个点!

函数 copy 从源 slice src 复制元素到目标dst，并且返回复制的元素的个数。
var a=[...]int{0,1,2,3,4,5,6,7}
var s = make([]int, 6)  // slice不能用new，smake([]T, len, cap)
n1 := copy(s, a[0:])      //n1 == 6, s == []int{0, 1, 2, 3, 4, 5} 
n2 := copy(s, s[2:])     //n2 == 4, s == []int{2, 3, 4, 5, 4, 5}

# map

一般定义 map 的方法是:
map[<from type>]<to type>

当只要声明一个map时：
monthdays := make(map[string]int)
monthdays := map[string]int {
​    "Jan": 31, "Feb": 28, "Mar": 31,
​    "Apr": 30, "May": 31, "Jun": 30,
​    "Jul": 31, "Aug": 31, "Sep": 30,
​    "Oct": 31, "Nov": 30, "Dec": 31, // 最后一个逗号，不能省略
}

向 map 增加元素:
monthdays["Undecim"] = 30

检查元素是否存在:
v, ok := monthdays["Jan"]      //v=31, ok=true

从 map 中移除元素:
delete(monthdays, "Undecim")

# 函数

func (p mytype) funcname(q int) (r, s int) {return 0,0}

func: 关键字 func 用于定义一个函数;
(p mytype): 函数可以绑定到特定的类型上。这叫做接收者。有接收者的函数被称作 method;
funcname: 函数的名字;
(q int): int类型的变量q作为输入参数。参数用pass-by-value方式传递，意味着它们会被复制;
(r, s int): 变量 r 和 s 是这个函数的 命名返回值。在 Go 的函数中可以返回多个值。
如果不想对返回的参数命名，只需要提供类型:(int,int)。
如果只有一个返回值，可以省略圆括号。
如果函数是一个子过程，并且没有任何返回值，也可以省略这些内容;
函数体.

可以随意安排函数定义的顺序，编译器会在执行前扫描每个文件。所以函数原型在 Go 中都是过期的旧物。Go 不允许函数嵌套，然而你可以利用匿名函数实现它.
在 Go 中，定义在函数外的变量是全局的，那些定义在函数内部的变量，对于函数来说是局部的。如果命名覆盖——一个局部变量与一个全局变量有相同的名字——在函数执行的时候，局部变量将覆盖全局变量。
延迟代码：在 defer 后指定的 函数会在函数退出前调用。
可以将多个函数放入 “延迟列表”中，延迟的函数是按照后进先出(LIFO)的顺序执行。
利用 defer 甚至可以修改返回值：

```go
func fun() (ret int) {
    defer func(ans int) {   // 将函数fun()的返回值加1
        fmt.Printf("%d\n", ans)
        ret++
    } (3)  //必须加，为ans赋值3.相当于调用func（3）
    return 0
}  // 返回结果为1，而不是0
```

接受不定数量的参数的函数叫做变参函数。定义函数使其接受变参:
func myfunc(arg ...int) { }

arg ...int 告诉 Go 这个函数接受不定数量的参数。注意，这些参数的类型全部是 int。
在函数体中，变量 arg 是一个 int 类型的 slice。
函数也是值，可以像下面这样赋值给变量:
func main() {
​    a := func() {         ／／定义一个匿名函数并赋值给变量a
​        println("Hello")
​    }
​    a()                        ／／调用函数
}

函数是值，可以很容易的传递到其他函数里，然后可以作为回调。
func printit(x int) {  // 函数无返回值 
​    fmt.Printf("%v\n", x)  // 仅仅打印
}

这个函数的标识是 func printit(int)，或者没有函数名的:func(int)。创建新的函数使用这个作为回调，需要用到这个标识:
func callback(y int, f func(int)) { // f 将会保存函数 
​    f(y) // 调用回调函数 f 输入变量 y
}

Go 没有异常机制，无法抛出一个异常。作为替 代，它使用了恐慌和恢复(panic-and-recover)机制。
panic()

是一个内建函数，可以中断原有的控制流程，进入一个令人恐慌的流程中。当函 数 F 调用 panic，函数 F 的执行被中断，并且 F 中的延迟函数会正常执行，然 后 F 返回到调用它的地方。在调用的地方，F 的行为就像调用了 panic。这一过 程继续向上，直到程序崩溃时的所有 goroutine 返回。
恐慌可以直接调用 panic 产生。也可以由运行时错误产生，例如访问越界的数 组。
recover()

是一个内建的函数，可以让进入令人恐慌的流程中的 goroutine 恢复过来。recover 仅在延迟函数中有效。
在正常的执行过程中，调用 recover 会返回 nil 并且没有其他任何效果。如果 当前的 goroutine 陷入恐慌，调用 recover 可以捕获到 panic 的输入值，并且恢 复正常的执行。
func throwsPanic(f func()) (b bool) {//定义一个新函数 throwsPanic 接受一个函数作为参数。函数 f 产生 panic，就返回 true，否则返回 false;
​    defer func() { 
​    //定义了一个利用 recover 的 defer 函数。
​    // 如果当前的 goroutine 产生了 panic，这个 defer 函数能够发现。
​    // 当 recover() 返回非 nil 值，设置 b 为 true;
​        if x := recover(); x != nil { 
​            b = true
​        } 
​    }()
​    f()    //调用作为参数接收的函数。
​    return //返回 b 的值。由于 b 是命名返回值，无须指定 b。
}

# 包

包是函数和数据的集合。用 package 关键字定义一个包。文件名不需要与包名一致。包名的约定是使用小写字符。Go 包可以由多个文件组成，但是使用相同的 package <name> 这一行。
名称以大写字母起始的函数是可导出的，可以在包的外部调用；名称以小写字母起始的函数则是私有的，外部不可调用。
概括来说:

公有函数的名字以大写字母开头;
私有函数的名字以小写字母开头。

这个规则同样适用于定义在包中的其他名字(新类型、全局变量)。
构建自定义的包even.go :
$ mkdir $GOPATH/src/even
$ cp even.go $GOPATH/src/even 
$ go build
$ go install

构建好包后，则可以在程序中使用该包，
1、导入包：import "even"
2、调用函数：访问一个包中的函数的语法是 <package>.Function()：even.Even()

包名是导入的默认名称。可以通过在导入语句指定其他名称来覆盖默认名称:
import bar "bytes"

每个包都应该有包注释，在 package 前的一个注释块。对于多文件包，包注释只需要 出现在一个文件前，任意一个文件都可以。包注释应当对包进行介绍，并提供相关于 包的整体信息。这会出现在 go doc 生成的关于包的页面上，并且相关的细节会一并 显示。
每个定义(并且导出)的函数应当有一小段文字描述该函数的行为。
测试包
编写测试需要包含testing包和程序go test。
测试文件也在包目录中，被命名为 *_test.go。这些测试文件同 Go 程序中的其他文件一样，但是 go test 只会执行测试函数。每个测试函数都有相同的标识，它的名字以 Test 开头:
func TestXxx(t *testing.T)

编写测试时，需要告诉 go test 测试是失败还是成功。测试成功则直接返回。当测试失败可以用的函数标记.
func (t *T) Fail()

Fail 标记测试函数失败，但仍然继续执行。
func (t *T) FailNow()

FailNow 标记测试函数失败，并且中断其执行。当前文件中的其余的测试将被跳过，然后执行下一个文件中的测试。
func (t *T) Log(args ...interface { })

Log 用默认格式对其参数进行格式化，与 Print()类似，并且记录文本到错误日志。
func (t *T) Fatal(args ...interface { })

Fatal 等价于 Log() 后跟随 FailNow()。
//even.go
package even 
import "testing"            // 导入测试包
func TestEven(t *testing.T) { 
​    if ! Even(2) { 
​        t.Log("2 should be even!") 
​        t.Fail()
​    }
}

执行测试:
$ go test

常用的包：

# fmt

包 fmt 实现了格式化的 I/O 函数，一些短语(%-序列)这样使用:
%v：默认格式的值。当打印结构时，加号(%+v)会增加字段名; 
%#v：Go 样式的值表达; 
%T：带有类型的 Go 样式的值表达;

# flag

flag包实现了命令行参数的解析。

注册：
使用flag.String(), Bool(), Int()等函数注册flag，下例声明了一个整数flag，解析结果保存在*int指针ip里：

import "flag"
var ip = flag.Int("flagname", 1234, "help message for flagname")

也可以将flag绑定到一个变量，使用Var系列函数：
var flagvar int
func init() {
​    flag.IntVar(&flagvar, "flagname", 1234, "help message for flagname")
}

解析：
解析命令行参数写入注册的flag里：

flag.Parse()

解析后，flag后面的参数可以从flag.Args()里获取或用flag.Arg(i)单独获取。这些参数的索引为从0到flag.NArg()-1。

# bufio

bufio 包实现了缓存IO。它包装了 io.Reader 和 io.Writer 对象，创建了另外的Reader和Writer对象，它们也实现了io.Reader和io.Writer接口，不过它们是有缓存的。该包同时为文本I/O提供了一些便利操作。

Reader 类型和方法

Reader结构
type Reader struct {
​    buf          []byte     // 缓存
​    rd           io.Reader  // 底层的io.Reader
​    r, w         int
​    err          error      // 读过程中遇到的错误
​    lastByte     int        // 最后一次读到的字节
​    lastRuneSize int        // 最后一次读到的Rune的大小
}

NewReaderSize方法
func NewReaderSize(rd io.Reader, size int) *Reader

作用：
NewReaderSize 将 rd 封装成一个带缓存的 bufio.Reader 对象，缓存大小由 size 指定（如果小于 16 则会被设置为 16）。 如果 rd 的基类型就是有足够缓存的 bufio.Reader 类型，则直接将 rd 转换为基类型返回。
NewReader方法
func NewReader(rd io.Reader) *Reader

NewReader 相当于 NewReaderSize(rd, 4096)

# Peek方法

func (b *Reader) Peek(n int) ([]byte, error)

Peek 返回缓存的一个切片，该切片引用缓存中前 n 个字节的数据，该操作不会将数据读出，只是引用，引用的数据在下一次读取操作之前是有效的。
如果切片长度小于 n，则返回一个错误信息说明原因。
如果 n 大于缓存的总大小，则返回 ErrBufferFull。

# Read方法

func (b *Reader) Read(p []byte) (n int, err error)

Read 从 b 中读出数据到 p 中，返回读出的字节数和遇到的错误。    如果缓存不为空，则只能读出缓存中的数据，不会从底层 io.Reader中提取数据，如果缓存为空，则：

len(p) >= 缓存大小，则跳过缓存，直接从底层 io.Reader 中读出到 p 中。
len(p) < 缓存大小，则先将数据从底层 io.Reader 中读取到缓存中，再从缓存读取到 p 中。

# Buffered方法

func (b *Reader) Buffered() int

Buffered 返回缓存中未读取的数据的长度。

# Discard方法

func (b *Reader) Discard(n int) (discarded int, err error)

Discard 跳过后续的 n 个字节的数据，返回跳过的字节数。
如果结果小于 n，将返回错误信息。
如果 n 小于缓存中的数据长度，则不会从底层提取数据。

# Writer 类型和方法

**writer结构**

type Writer struct {
​    err error       // 写过程中遇到的错误
​    buf []byte      // 缓存
​    n   int         // 当前缓存中的字节数
​    wr  io.Writer   // 底层的 io.Writer 对象
}

**NewWriterSize**
func NewWriterSize(wr io.Writer, size int) *Writer

NewWriterSize 将 wr 封装成一个带缓存的 bufio.Writer 对象，缓存大小由 size 指定（如果小于 4096 则会被设置为 4096）。如果 wr 的基类型就是有足够缓存的 bufio.Writer 类型，则直接将wr 转换为基类型返回。
**NewWriter**
func NewWriter(wr io.Writer) *Writer

NewWriter 相当于 NewWriterSize(wr, 4096)
**WriteString**
func (b *Writer) WriteString(s string) (int, error)

WriteString 功能同 Write，只不过写入的是字符串
**WriteRune**
func (b *Writer) WriteRune(r rune) (size int, err error)

WriteRune 向 b 写入 r 的 UTF-8 编码，返回 r 的编码长度
**Flush**
func (b *Writer) Flush() error

Flush 将缓存中的数据提交到底层的 io.Writer 中
**Available**
func (b *Writer) Available() int

Available 返回缓存中未使用的空间的长度
**Buffered**
func (b *Writer) Buffered() int

Buffered 返回缓存中未提交的数据的长度
**Reset**
func (b *Writer) Reset(w io.Writer)

Reset 将 b 的底层 Writer 重新指定为 w，同时丢弃缓存中的所有数据，复位所有标记和错误信息。相当于创建了一个新的 bufio.Writer。

# Scanner 类型和方法

scanner := bufio.NewScanner(os.Stdin)
for scanner.Scan() {
​    ucl := strings.ToUpper(scanner.Text())
​    fmt.Println(ucl)
}
if err := scanner.Err(); err != nil {
​    fmt.Fprintln(os.Stderr, "error:", err)
​    os.Exit(1)
}

# os

os.Getwd()函数
原型：func Getwd()(pwd string, err error)
作用：获取当前文件路径
返回：当前文件路径的字符串和一个err信息
os.Getenv()函数
原型：func Getenv(key string) string
作用：获取系统环境变量的值
参数：key - 系统环境变量名
返回：系统环境变量的值
os.Chdir()函数
原型：func Chdir(dir string) error
作用：将当前文件路径改变为目标路径（非真实改变）
参数：dir - 目标路径（即改变之后的路径）
返回：修改成功，返回 nil；修改失败（如：目标路径不存在的情况），返回错误信息。
os.Open()函数
原型：func Open(name string) (file *File, err error)
作用：打开一个文件
参数：name - 文件名
返回：返回文件描述符，该文件描述符只有只读权限，相当于OpenFile(name string,O_RDWR,0)

# 指针

Go 有指针,然而却没有指针运算.
通过类型作为前缀来定义一个指针’*’:
var p *int。

一个新定义的或者没有任何指向的指针，有值 nil。
让指针指向某些内容，可以使用取址操作符 (&):
var I int 
p = &I
*p = 8

内存分配
Go 有垃圾收集机制，也就是说无须担心内存分配和回收。
Go 有两个内存分配原语，new 和 make。
new(T) 分配了零值填充的T类型的内存空间，并且返回其地址，一个 *T 类型的值。用 Go 的术语说，它返回 了一个指针，指向新分配的类型 T 的零值。
make(T, args) 只能创建 slice，map 和 channel，并且返回一个有初始值(非零)的 T 类型，而不是 *T。本质 来讲，导致这三个类型有所不同的原因是指向数据结构的引用在使用前必须被初始化。 例如，一个 slice，是一个包含指向数据(内部 array)的指针，长度和容量的三项描述 符;在这些项目被初始化之前，slice 为 nil。对于 slice，map 和 channel，make 初始 化了内部的数据结构，填充适当的值。

# 定义自己的类型

Go 允许定义新的类型，通过关键字 type 实现:
type foo int

struct:
type NameAge struct {
​    name string
​    age int
}

结构字段:首字母大写的字段可以被导出，也就是说，在其他包中可以进行读写。字段名以 小写字母开头是当前包的私有的。
方法:可以对新定义的类型创建函数以便操作，可以通过两种途径:

创建一个函数接受这个类型的参数。

func doSomething(n1 *NameAge, n2 int) { /* */ }

这是 函数调用。

创建一个工作在这个类型上的函数:

func (n1 *NameAge) doSomething(n2 int) { /* */ }

这是方法调用，可以类似这样使用:
var n *NameAge n.doSomething(2)

如果 x 可获取地址，并且 &x 的方法中包含了 m，x.m() 是 (&x).m() 更短的写法。
var n NameAge    // 不是指针
n.doSomething(2)

这里 Go 会查找 NameAge 类型的变量 n 的方法列表，没有找到就会再查找 *NameAge类型的方法列表，并且将其转化为 (&n).doSomething(2)。
两种不同的风格创建了两个数据类型。

type NewMutex Mutex;
type PrintableMutex struct {Mutex }.

现在 NewMutux 等同于 Mutex，但是它没有任何 Mutex 的方法。换句话说，它的方法 是空的。
但是 PrintableMutex 已经从 Mutex 继承了方法集合。

# 转化![1553064656774](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1553064656774.png)


从 string 到字节或者 rune 的 slice

mystring := "hello this is string"
byteslice := []byte(mystring)    //转换到 byte slice，每个 byte 保存字符串对应字节的整数值
runeslice := []rune(mystring)   //转换到 rune slice，每个 rune 保存 Unicode 编码的指针。字符串中的每个字符对应一个整数。


从字节(byte)或者整形(rune)的 slice 到 string

b := []byte {'h','e','l','l','o'} // 复合声明 s := string(b)
i := []rune {257,1024,65}
r := string(i)



对于数值，定义了下面的转换:

将整数转换到指定的(bit)长度:uint8(int);
从浮点数到整数:int(float32)。这会截断浮点数的小数部分;
其他的类似:float32(int)。



# 接口

定义结构和方法：
type S struct { i  int }
func (p *S) Get() int { return p.i } 
func (p *S) Put(v int) { p.i=v }

定义接口类型，仅仅是方法的集合：
type I interface { 
​    Get() int 
​    Put(int)
}

定义一个函数接受一个接口类型作为参数; p实现了接口I，必须有Get()方法; Put()方法是类似的。
func f(p I) { 
​    fmt.Println(p.Get()) 
​    p.Put(1) 2
}

定义另外一个类型同样实现了接口 I:
type R struct { i int }
func (p *R) Get() int { return p.i } 
func (p *R) Put(v int) { p.i=v }

函数 f 现在可以接受类型为 R 或 S 的变量。在 Go 中可以使用 type switch 得到。
func f(p I) {
​    switch t := p.(type) {
​        case *S: ...
​        case *R: ...
​        case  S: ...
​        case  R: ...
​        default : ...  
​    }
}

在 switch 之外使用 (type) 是非法的。
判断一个接口类型是否实现了 某个特定接口:
i f t, ok := interfaceType.(I) ; ok { 
// 对于某些实现了接口 I 的 
// t 是其所拥有的类型
}

由于每个类型都能匹配到空接口: interface{}。我们可以创建一个接受空接口作为 参数的普通函数:
func g(something interface { }) int { 
​    if v, ok := something.(I); ok {
​        return something.(I).Get()
​    }
​    return -1
}

值 something 具有 类型 interface{}，这意味着方法没有任何约束:它能包含任何类型。.(I) 是类型断言，用于转换 something 到 I 类型的接口。如果有这个类型，则可以调用Get()函数。
接收者不能定义为接口类型，接收者类型必须是T或*T，这里的T是类型名。T 叫做接收者基础类型或简称基础类型。基础类型一定不能是指针或接口类型，并且定义在与方法 相同的包中。

# 反射

包reflect
reflect包有两个数据类型是最重要的，一个是Type，一个是Value。Type就是定义的类型的一个数据类型，Value是值的类型。
TypeOf和ValueOf是获取Type和Value的方法。
goroutine
goroutine 有简单的模型:它是与其他 goroutine 并行执行的， 有着相同地址空间的函数。它是轻量的，仅比分配栈空间多一点点 。 而初始时栈是很小的，所以它们也是廉价的，并且随着需要在堆空间上分配(和释放)。goroutine 是一个普通的函数，只是需要使用关键字 go 作为开头。
ready("Tea", 2)    // 普通函数调用
go ready("Tea", 2) // ready() 作为 goroutine 运行

如果不等待 goroutine 的执行，程序立刻终止，而任何正在执行的 goroutine 都会停止。
channels是能够同 goroutine 通讯的机制。可以通过channel发送或者接收值。这些值只能是特定的类型:channel 类型。定义一个 channel 时，也需要定义发送到 channel 的值的类型。注意，必须使用 make 创建 channel:
ci := make(chan int)    // 创建 channel ci 用于发送和接收整数
cs := make(chan string) // 创建 channel cs 用于字符串
cf := make(chan interface{})// channel cf 使用了空接口来满足各种类型

向 channel 发送或接收数据，是通过类似的操作符完成的:<−. 具体作用则依赖于操作符的位置:
ci <− 1   // 发送整数 1 到 channelci
<−ci      // 从 channel ci 接收整数
i := <−ci // 从 channel ci 接收整数，并保存到 i 中

通过 select(和其他东西)可以监听 channel 上输入的数据。
虽然 goroutine 是并发执行的，但是它们并不是并行运行的。如果不告诉 Go 额外的 东西，同一时刻只会有一个 goroutine 执行。利用 runtime.GOMAXPROCS(n) 可以设置 goroutine 并行执行的数量。
ch := make(chan type, value)
value == 0  // 无缓冲
value > 0   // 缓冲 value 的元素

x, ok = <−ch

当 ok 被赋值为 true 意味着 channel 尚未被关闭，同时 可以读取数据。否则 ok 被赋值为 false。在这个情况下表示 channel 被关闭。

# 通讯

I/O 核心是接口 io.Reader 和 io.Writer。
读写文件（无缓冲）：
buf := make([]byte, 1024)
f, _ := os.Open("/etc/passwd")
n, _ := f.Read(buf)
os.Stdout.Write(buf[:n])

读写文件（有缓冲）：
buf := make([]byte, 1024)
f, _ := os.Open("/etc/passwd")
r := bufio.NewReader(f) 1
w := bufio.NewWriter(os.Stdout)
n, _ := r.Read(buf) // s, ok := r.ReadString('\n')读取一行，还有ReadLine
w.Write(buf[0:n])

# 网络

所有网络相关的类型和函数可以在 net 包中找到。这其中最重要的函数是 Dial。
当 Dial 到远程系统，这个函数返回 Conn 接口类型，可以用于发送或接收信息。函数 Dial 简洁的抽象了网络层和传输层。因此 IPv4 或者 IPv6，TCP 或者 UDP 可以共用一 个接口。
conn, e := Dial("tcp", "192.0.32.10:80")  //  通过 TCP 连接到远程系统(端口 80)
conn, e := Dial("udp", "192.0.32.10:80")  //  通过 UDP 连接到远程系统(端口 80)
conn, e := Dial("tcp", "[2620:0:2d0:200::10]:80")    
// TCP 通过IPv6 连接到远程系统(端口 80)，方括号是强制的如果没有错误(由 e 返回)，
// 就可以使用 conn 从套接字中读写，conn 是 io.ReadWriter。

更高层次的包：net/http 包
r, err := http.Get("http://www.baidu.com/index.txt")
b, err := ioutil.ReadAll(r.Body)      // import "io/ioutil"
r.Body.Close()

