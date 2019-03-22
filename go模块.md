# flag

```go
//定义命令行参数 name:参数名string, value:参数默认值， usage:参数说明string
flag.<type>Var(name, value, usage)
var varname *string = flag.String(name, value, usage)
flag.Parse() //生效
```

## 1.2 flag 包概述

flag 包实现了命令行参数的解析。

### 1.2.1 定义 flags 有两种方式

1）flag.Xxx()，其中 Xxx 可以是 Int、String，Bool 等；返回一个相应类型的指针，如：
 `var ip = flag.Int("flagname", 1234, "help message for flagname")`

- 第一个参数 ：flag名称为flagname
- 第二个参数 ：flagname默认值为1234
- 第三个参数 ：flagname的提示信息

返回的ip是指针类型，所以这种方式获取ip的值应该`fmt.Println(*ip)`

2）flag.XxxVar()，将 flag 绑定到一个变量上，如：

```go
var flagValue int
flag.IntVar(&flagValue, "flagname", 1234, "help message for flagname")
```

- 第一个参数 ：接收flagname的实际值的
- 第二个参数 ：flag名称为flagname
- 第三个参数 ：flagname默认值为1234
- 第四个参数 ：flagname的提示信息
   这种方式获取ip的值`fmt.Println(ip)`就可以了：

### 1.2.2  自定义 Value

另外，还可以创建自定义 flag，只要实现 flag.Value 接口即可（要求 `receiver` 是指针），这时候可以通过如下方式定义该 flag：

```go
flag.Var(&flagVal, "name", "help message for flagname")
```

例如，解析我喜欢的编程语言，我们希望直接解析到 slice 中，我们可以定义如下 sliceValue类型，然后实现Value接口：

```go
package main

import (
    "flag"
    "fmt"
    "strings"
)

//定义一个类型，用于增加该类型方法
type sliceValue []string

//new一个存放命令行参数值的slice
func newSliceValue(vals []string, p *[]string) *sliceValue {
    *p = vals
    return (*sliceValue)(p)
}

/*
Value接口：
type Value interface {
    String() string
    Set(string) error
}
实现flag包中的Value接口，将命令行接收到的值用,分隔存到slice里
*/
func (s *sliceValue) Set(val string) error {
    *s = sliceValue(strings.Split(val, ","))
    return nil
}

//flag为slice的默认值default is me,和return返回值没有关系
func (s *sliceValue) String() string {
    *s = sliceValue(strings.Split("default is me", ","))
    return "It's none of my business"
}

/*
可执行文件名 -slice="java,go"  最后将输出[java,go]
可执行文件名 最后将输出[default is me]
 */
func main(){
    var languages []string
    flag.Var(newSliceValue([]string{}, &languages), "slice", "I like programming `languages`")
    flag.Parse()

    //打印结果slice接收到的值
    fmt.Println(languages)
}
```

这样通过 `-slice "go,php"` 这样的形式传递参数，`languages` 得到的就是 `[go, php]`。如果不加`-slice`参数则打印默认值`[default is me]`

flag 中对 `Duration` 这种非基本类型的支持，使用的就是类似这样的方式，即同样实现了`Value`接口。

### 1.2.3 解析 flag

在所有的 flag 定义完成之后，可以通过调用 `flag.Parse()` 进行解析。

命令行 flag 的语法有如下三种形式：

```
-flag // 只支持bool类型
-flag=x
-flag x // 只支持非bool类型
```

以上语法对于一个或两个‘－’号，效果是一样的，但是要注意对于第三种情况，只能用于非 bool 类型的 flag。原因是：如果支持，那么对于这样的命令 cmd -x *，如果有一个文件名字是：0或false等，则命令的原意会改变（bool 类型可以和其他类型一样处理，其次 bool 类型支持 `-flag` 这种形式，因为Parse()中，对 bool 类型进行了特殊处理）。默认的，提供了 `-flag`，则对应的值为 true，否则为 `flag.Bool/BoolVar` 中指定的默认值；如果希望显示设置为 false 则使用 `-flag=false`。

int 类型可以是十进制、十六进制、八进制甚至是负数；bool 类型可以是1, 0, t, f, true, false, TRUE, FALSE, True, False。Duration 可以接受任何 time.ParseDuration 能解析的类型。

- 注：如果bool类型的参数在命令行中用了`-flag false`这种形式时，其后的参数都会被当做非flag（non-flag）参数，non-flag 参数后面解释。

## 1.3 类型和函数

在看类型和函数之前，先看一下变量。

ErrHelp：该错误类型用于当命令行指定了 ·-help` 参数但没有定义时。

例如1.2.2例子中：如果执行时用了`-help`或者`-h`时就会输出help message：

```go
Usage of myflag.exe:
  -slice languages
        I like programming languages
```

Usage：这是一个函数，用于输出所有定义了的命令行参数和帮助信息（usage message）。一般，当命令行参数解析出错时，该函数会被调用。我们可以指定自己的 Usage 函数，即：`flag.Usage = func(){}`

例如1.1示例中：如果执行时用了`-help`时就会输出和`-h`一样的usage message。

### 1.3.1 函数

go标准库中，经常这么做：

> 定义了一个类型，提供了很多方法；为了方便使用，会实例化一个该类型的实例（通用），这样便可以直接使用该实例调用方法。比如：encoding/base64 中提供了 StdEncoding 和 URLEncoding 实例，使用时：base64.StdEncoding.Encode()

在 flag 包使用了有类似的方法，比如 CommandLine 变量，只不过 flag 进行了进一步封装：将 FlagSet 的方法都重新定义了一遍，也就是提供了一系列函数，而函数中只是简单的调用已经实例化好了的 FlagSet 实例：CommandLine 的方法。这样，使用者是这么调用：flag.Parse() 而不是 flag. CommandLine.Parse()。（Go 1.2 起，将 CommandLine 导出，之前是非导出的）

这里不详细介绍各个函数，其他函数介绍可以参考[astaxie的gopkg——flag章节。](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fastaxie%2Fgopkg%2Fblob%2Fmaster%2Fflag)

### 1.3.2 类型（数据结构）

1）ErrorHandling

```go
type ErrorHandling int
```

该类型定义了在参数解析出错时错误处理方式。定义了三个该类型的常量：

```go
const (
    ContinueOnError ErrorHandling = iota
    ExitOnError
    PanicOnError
)
```

三个常量在源码的 FlagSet 的方法 parseOne() 中使用了。

2）Flag

```go
// A Flag represents the state of a flag.
type Flag struct {
    Name     string // name as it appears on command line
    Usage    string // help message
    Value    Value  // value as set
    DefValue string // default value (as text); for usage message
}
```

Flag 类型代表一个 flag 的状态。

比如，对于命令：`./nginx -c /etc/nginx.conf`，相应代码是：

```go
flag.StringVar(&c, "c", "conf/nginx.conf", "set configuration `file`")
```

则该 Flag 实例（可以通过 `flag.Lookup("c")` 获得）相应各个字段的值为：

```go
&Flag{
    Name: c,
    Usage: set configuration file,
    Value: /etc/nginx.conf,
    DefValue: conf/nginx.conf,
}
```

Lookup函数：获取flag集合中名称为name值的flag指针，如果对应的flag不存在，返回nil
 **示例：**

```go
package main

import (
    "flag"
    "fmt"
)

//定义一个全局变量的命令行接收参数
var testFlag = flag.String("test", "default value", "help message.")

//打印值的函数
func print(f *flag.Flag) {
    if f != nil {
        fmt.Println(f.Value)
    } else {
        fmt.Println(nil)
    }
}

func main() {
    //没有用flag.Parse()解析前
    fmt.Print("test:")
    print(flag.Lookup("test"))
    fmt.Print("test1:")
    print(flag.Lookup("test1"))

    //用flag.Parse()解析后
    flag.Parse()
    fmt.Print("test:")
    print(flag.Lookup("test"))
    fmt.Print("test1:")
    print(flag.Lookup("test1"))
}
```

运行结果：

```go
//  ./testlookup -test "12345"      
test:default value
test1:<nil>
test:12345
test1:<nil>
```

3）FlagSet

```go
// A FlagSet represents a set of defined flags.
type FlagSet struct {
    // Usage is the function called when an error occurs while parsing flags.
    // The field is a function (not a method) that may be changed to point to
    // a custom error handler.
    Usage func()

    name string // FlagSet的名字。CommandLine 给的是 os.Args[0]
    parsed bool // 是否执行过Parse()
    actual map[string]*Flag // 存放实际传递了的参数（即命令行参数）
    formal map[string]*Flag // 存放所有已定义命令行参数
    args []string // arguments after flags // 开始存放所有参数，最后保留 非flag（non-flag）参数
    exitOnError bool // does the program exit if there's an error?
    errorHandling ErrorHandling // 当解析出错时，处理错误的方式
    output io.Writer // nil means stderr; use out() accessor
}
```

4）Value 接口

```go
// Value is the interface to the dynamic value stored in a flag.
// (The default value is represented as a string.)
type Value interface {
    String() string
    Set(string) error
}
```

所有参数类型需要实现 Value 接口，flag 包中，为int、float、bool等实现了该接口。借助该接口，我们可以自定义flag。（上文已经给了具体的例子）

## 1.4 主要类型的方法（包括类型实例化）

flag 包中主要是 FlagSet 类型。

### 1.4.1 实例化方式

`NewFlagSet()` 用于实例化 FlagSet。预定义的 FlagSet 实例 `CommandLine` 的定义方式：

```go
// The default set of command-line flags, parsed from os.Args.
var CommandLine = NewFlagSet(os.Args[0], ExitOnError)
```

可见，默认的 FlagSet 实例在解析出错时会退出程序。

由于 FlagSet 中的字段没有 export，其他方式获得 FlagSet实例后，比如：FlagSet{} 或 new(FlagSet)，应该调用Init() 方法，以初始化 name 和 errorHandling，否则 name 为空，errorHandling 为 ContinueOnError（errorHandling默认为0）。

### 1.4.2  定义 flag 参数的方法

这一系列的方法都有两种形式，在一开始已经说了两种方式的区别。这些方法用于定义某一类型的 flag 参数。

### 1.4.3 解析参数（Parse）

```go
func (f *FlagSet) Parse(arguments []string) error
```

从参数列表中解析定义的 flag。方法参数 arguments 不包括命令名，即应该是os.Args[1:]。事实上，`flag.Parse()` 函数就是这么做的：

```go
// Parse parses the command-line flags from os.Args[1:].  Must be called
// after all flags are defined and before flags are accessed by the program.
func Parse() {
    // Ignore errors; CommandLine is set for ExitOnError.
    CommandLine.Parse(os.Args[1:])
}
```

该方法应该在 flag 参数定义后而具体参数值被访问前调用。

如果提供了 `-help` 参数（命令中给了）但没有定义（代码中没有），该方法返回 `ErrHelp` 错误。默认的 CommandLine，在 Parse 出错时会退出程序（ExitOnError）。

为了更深入的理解，我们看一下 `Parse(arguments []string)` 的源码：

```go
func (f *FlagSet) Parse(arguments []string) error {
    f.parsed = true
    f.args = arguments
    for {
        seen, err := f.parseOne()
        if seen {
            continue
        }
        if err == nil {
            break
        }
        switch f.errorHandling {
        case ContinueOnError:
            return err
        case ExitOnError:
            os.Exit(2)
        case PanicOnError:
            panic(err)
        }
    }
    return nil
}
```

真正解析参数的方法是非导出方法 `parseOne`。

结合 `parseOne` 方法，我们来解释 `non-flag` 以及包文档中的这句话：

> Flag parsing stops just before the first non-flag argument ("-" is a non-flag argument) or after the terminator "--".

我们需要了解解析什么时候停止。

根据 Parse() 中 for 循环终止的条件（不考虑解析出错），我们知道，当 parseOne 返回 `false, nil` 时，Parse 解析终止。正常解析完成我们不考虑。看一下 parseOne 的源码发现，有三处会返回 `false, nil`。
 在这里先说一下non-flag命令行参数是指不满足命令行语法的参数，如命令行参数为cmd -flag=true abc则第一个非flag命令行参数为“abc”

1）参数列表长度为0

```go
if len(f.args) == 0 {
        return false, nil
}
```

2）第一个 non-flag 参数

```go
s := f.args[0]
if len(s) == 0 || s[0] != '-' || len(s) == 1 {
    return false, nil
}
```

也就是，当遇到单独的一个"-"或不是"-"开始时，会停止解析。比如：

> ./nginx - 或 ./nginx ba或者./nginx

这两种情况，`-c` 都不会被正确解析。像该例子中的"-"或ba（以及之后的参数），我们称之为 `non-flag`参数。

3）两个连续的"--"

```go
if s[1] == '-' {
    num_minuses++
    if len(s) == 2 { // "--" terminates the flags
        f.args = f.args[1:]
        return false, nil
    }
}
```

也就是，当遇到连续的两个"-"时，解析停止。如：

> ./nginx --

*下面这种情况是可以正常解析的：

> ./nginx  -c  --

这里的"--"会被当成是 `c` 的值

parseOne 方法中接下来是处理 `-flag=x` 这种形式，然后是 `-flag` 这种形式（bool类型）（这里对bool进行了特殊处理），接着是 `-flag x` 这种形式，最后，将解析成功的 Flag 实例存入 FlagSet 的 actual map 中。

另外，在 parseOne 中有这么一句：

```go
f.args = f.args[1:]
```

也就是说，每执行成功一次 parseOne，f.args 会少一个。所以，FlagSet 中的 args 最后留下来的就是所有 `non-flag` 参数。

### 1.4.4 Arg(i int) 和 Args()、NArg()、NFlag()

Arg(i int) 和 Args() 这两个方法就是获取 `non-flag` 参数的；NArg()获得 `non-flag` 的个数；NFlag() 获得 FlagSet 中 actual 长度（即被设置了的参数个数）。

### 1.4.5 Visit/VisitAll

这两个函数分别用于访问 FlatSet 的 actual（存放参数值实际Flag的map） 和 formal（存放参数名默认Flag的map） 中的 Flag，而具体的访问方式由调用者决定。

具体使用demo见:
 [func (f *FlagSet) Visit(fn func(*Flag))](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fastaxie%2Fgopkg%2Fblob%2Fmaster%2Fflag%2FFlagSetVisit.md)
 [func (f *FlagSet) VisitAll(fn func(*Flag))](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fastaxie%2Fgopkg%2Fblob%2Fmaster%2Fflag%2FFlagSetVisitAll.md)

### 1.4.6 PrintDefaults()

打印所有已定义参数的默认值（调用 VisitAll 实现），默认输出到标准错误，除非指定了 FlagSet 的 output（通过SetOutput() 设置）。
 **在1.1示例中有使用。还可以参考:**
 [func PrintDefaults()](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fastaxie%2Fgopkg%2Fblob%2Fmaster%2Fflag%2FPrintDefaults.md)

### 1.4.7 Set(name, value string)

将名称为name的flag的值设置为value, 成功返回nil。
 **demo请见：**
 [func Set(name, value string) error](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fastaxie%2Fgopkg%2Fblob%2Fmaster%2Fflag%2FSet.md)

## 1.5 总结

使用建议：虽然上面讲了那么多，一般来说，我们只简单的定义flag，然后 parse，就如同开始的例子一样。

如果项目需要复杂或更高级的命令行解析方式，可以使用 [https://github.com/urfave/cli](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Furfave%2Fcli) 或者 [https://github.com/spf13/cobra](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fspf13%2Fcobra) 这两个强大的库。

作者：我的小碗汤

链接：https://www.jianshu.com/p/f9cf46a4de0e

来源：简书

简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

# archive/tar

## package tar

```
import "archive/tar"
```

tar包实现了tar格式压缩文件的存取。本包目标是覆盖大多数tar的变种，包括GNU和BSD生成的tar文件。

参见：

```
http://www.freebsd.org/cgi/man.cgi?query=tar&sektion=5
http://www.gnu.org/software/tar/manual/html_node/Standard.html
http://pubs.opengroup.org/onlinepubs/9699919799/utilities/pax.html
```

Example

```go
// Create a buffer to write our archive to.
buf := new(bytes.Buffer)
// Create a new tar archive.
tw := tar.NewWriter(buf)
// Add some files to the archive.
var files = []struct {
    Name, Body string
}{
    {"readme.txt", "This archive contains some text files."},
    {"gopher.txt", "Gopher names:\nGeorge\nGeoffrey\nGonzo"},
    {"todo.txt", "Get animal handling licence."},
}
for _, file := range files {
    hdr := &tar.Header{
        Name: file.Name,
        Size: int64(len(file.Body)),
    }
    if err := tw.WriteHeader(hdr); err != nil {
        log.Fatalln(err)
    }
    if _, err := tw.Write([]byte(file.Body)); err != nil {
        log.Fatalln(err)
    }
}
// Make sure to check the error on Close.
if err := tw.Close(); err != nil {
    log.Fatalln(err)
}
// Open the tar archive for reading.
r := bytes.NewReader(buf.Bytes())
tr := tar.NewReader(r)
// Iterate through the files in the archive.
for {
    hdr, err := tr.Next()
    if err == io.EOF {
        // end of tar archive
        break
    }
    if err != nil {
        log.Fatalln(err)
    }
    fmt.Printf("Contents of %s:\n", hdr.Name)
    if _, err := io.Copy(os.Stdout, tr); err != nil {
        log.Fatalln(err)
    }
    fmt.Println()
}
```

Output:

```go
Contents of readme.txt:
This archive contains some text files.
Contents of gopher.txt:
Gopher names:
George
Geoffrey
Gonzo
Contents of todo.txt:
Get animal handling licence.
```

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#pkg-constants)

[Variables](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#pkg-variables)

[type Header](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Header)

- [func FileInfoHeader(fi os.FileInfo, link string) (*Header, error)](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#FileInfoHeader)
- [func (h *Header) FileInfo() os.FileInfo](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Header.FileInfo)

[type Reader](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Reader)

- [func NewReader(r io.Reader) *Reader](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#NewReader)
- [func (tr *Reader) Next() (*Header, error)](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Reader.Next)
- [func (tr *Reader) Read(b\ [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Reader.Read)

[type Writer](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Writer)

- [func NewWriter(w io.Writer) *Writer](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#NewWriter)
- [func (tw *Writer) WriteHeader(hdr *Header) error](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Writer.WriteHeader)
- [func (tw *Writer) Write(b \[\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Writer.Write)
- [func (tw *Writer) Flush() error](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Writer.Flush)
- [func (tw *Writer) Close() error](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#Writer.Close)

#### Examples

返回首页



[package](https://studygolang.com/static/pkgdoc/pkg/archive_tar.htm#example-package)

### Constants

```go
const (
    // 类型
    TypeReg           = '0'    // 普通文件
    TypeRegA          = '\x00' // 普通文件
    TypeLink          = '1'    // 硬链接
    TypeSymlink       = '2'    // 符号链接
    TypeChar          = '3'    // 字符设备节点
    TypeBlock         = '4'    // 块设备节点
    TypeDir           = '5'    // 目录
    TypeFifo          = '6'    // 先进先出队列节点
    TypeCont          = '7'    // 保留位
    TypeXHeader       = 'x'    // 扩展头
    TypeXGlobalHeader = 'g'    // 全局扩展头
    TypeGNULongName   = 'L'    // 下一个文件记录有个长名字
    TypeGNULongLink   = 'K'    // 下一个文件记录指向一个具有长名字的文件
    TypeGNUSparse     = 'S'    // 稀疏文件
)
```

### Variables

```go
var (
    ErrWriteTooLong    = errors.New("archive/tar: write too long")
    ErrFieldTooLong    = errors.New("archive/tar: header field too long")
    ErrWriteAfterClose = errors.New("archive/tar: write after close")
)
var (
    ErrHeader = errors.New("archive/tar: invalid tar header")
)
```

### type [Header](https://github.com/golang/go/blob/master/src/archive/tar/common.go?name=release#46)

```go
type Header struct {
    Name       string    // 记录头域的文件名
    Mode       int64     // 权限和模式位
    Uid        int       // 所有者的用户ID
    Gid        int       // 所有者的组ID
    Size       int64     // 字节数（长度）
    ModTime    time.Time // 修改时间
    Typeflag   byte      // 记录头的类型
    Linkname   string    // 链接的目标名
    Uname      string    // 所有者的用户名
    Gname      string    // 所有者的组名
    Devmajor   int64     // 字符设备或块设备的major number
    Devminor   int64     // 字符设备或块设备的minor number
    AccessTime time.Time // 访问时间
    ChangeTime time.Time // 状态改变时间
    Xattrs     map[string]string
}
```

Header代表tar档案文件里的单个头。Header类型的某些字段可能未使用。

#### func [FileInfoHeader](https://github.com/golang/go/blob/master/src/archive/tar/common.go?name=release#204)

```go
func FileInfoHeader(fi os.FileInfo, link string) (*Header, error)
```

FileInfoHeader返回一个根据fi填写了部分字段的Header。 如果fi描述一个符号链接，FileInfoHeader函数将link参数作为链接目标。如果fi描述一个目录，会在名字后面添加斜杠。因为os.FileInfo接口的Name方法只返回它描述的文件的无路径名，有可能需要将返回值的Name字段修改为文件的完整路径名。

#### func (*Header) [FileInfo](https://github.com/golang/go/blob/master/src/archive/tar/common.go?name=release#71)

```go
func (h *Header) FileInfo() os.FileInfo
```

FileInfo返回该Header对应的文件信息。（os.FileInfo类型）

### type [Reader](https://github.com/golang/go/blob/master/src/archive/tar/reader.go?name=release#31)

```go
type Reader struct {
    // 内含隐藏或非导出字段
}
```

Reader提供了对一个tar档案文件的顺序读取。一个tar档案文件包含一系列文件。Next方法返回档案中的下一个文件（包括第一个），返回值可以被视为io.Reader来获取文件的数据。

#### func [NewReader](https://github.com/golang/go/blob/master/src/archive/tar/reader.go?name=release#84)

```go
func NewReader(r io.Reader) *Reader
```

NewReader创建一个从r读取的Reader。

#### func (*Reader) [Next](https://github.com/golang/go/blob/master/src/archive/tar/reader.go?name=release#87)

```go
func (tr *Reader) Next() (*Header, error)
```

转入tar档案文件下一记录，它会返回下一记录的头域。

#### func (*Reader) [Read](https://github.com/golang/go/blob/master/src/archive/tar/reader.go?name=release#726)

```go
func (tr *Reader) Read(b []byte) (n int, err error)
```

从档案文件的当前记录读取数据，到达记录末端时返回(0, EOF)，直到调用Next方法转入下一记录。

### type [Writer](https://github.com/golang/go/blob/master/src/archive/tar/writer.go?name=release#34)

```go
type Writer struct {
    // 内含隐藏或非导出字段
}
```

Writer类型提供了POSIX.1格式的tar档案文件的顺序写入。一个tar档案文件包含一系列文件。调用WriteHeader来写入一个新的文件，然后调用Write写入文件的数据，该记录写入的数据不能超过hdr.Size字节。

#### func [NewWriter](https://github.com/golang/go/blob/master/src/archive/tar/writer.go?name=release#45)

```go
func NewWriter(w io.Writer) *Writer
```

NewWriter创建一个写入w的*Writer。

#### func (*Writer) [WriteHeader](https://github.com/golang/go/blob/master/src/archive/tar/writer.go?name=release#136)

```go
func (tw *Writer) WriteHeader(hdr *Header) error
```

WriteHeader写入hdr并准备接受文件内容。如果不是第一次调用本方法，会调用Flush。在Close之后调用本方法会返回ErrWriteAfterClose。

#### func (*Writer) [Write](https://github.com/golang/go/blob/master/src/archive/tar/writer.go?name=release#343)

```go
func (tw *Writer) Write(b []byte) (n int, err error)
```

Write向tar档案文件的当前记录中写入数据。如果写入的数据总数超出上一次调用WriteHeader的参数hdr.Size字节，返回ErrWriteTooLong错误。

#### func (*Writer) [Flush](https://github.com/golang/go/blob/master/src/archive/tar/writer.go?name=release#48)

```go
func (tw *Writer) Flush() error
```

Flush结束当前文件的写入。（可选的）

#### func (*Writer) [Close](https://github.com/golang/go/blob/master/src/archive/tar/writer.go?name=release#365)

```go
func (tw *Writer) Close() error
```

Close关闭tar档案文件，会将缓冲中未写入下层的io.Writer接口的数据刷新到下层。

# archive/zip

## package zip

```
import "archive/zip"
```

zip包提供了zip档案文件的读写服务。参见<http://www.pkware.com/documents/casestudies/APPNOTE.TXT>

本包不支持跨硬盘的压缩。

关于ZIP64：

为了向下兼容，FileHeader同时拥有32位和64位的Size字段。64位字段总是包含正确的值，对普通格式的档案未见它们的值是相同的。对zip64格式的档案文件32位字段将是0xffffffff，必须使用64位字段。

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#pkg-constants)

[Variables](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#pkg-variables)

[type Compressor](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#Compressor)

[type Decompressor](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#Decompressor)

[func RegisterCompressor(method uint16, comp Compressor)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#RegisterCompressor)

[func RegisterDecompressor(method uint16, d Decompressor)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#RegisterDecompressor)

[type FileHeader](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#FileHeader)

- [func FileInfoHeader(fi os.FileInfo) (*FileHeader, error)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#FileInfoHeader)
- [func (h *FileHeader) FileInfo() os.FileInfo](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#FileHeader.FileInfo)
- [func (h *FileHeader) Mode() (mode os.FileMode)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#FileHeader.Mode)
- [func (h *FileHeader) SetMode(mode os.FileMode)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#FileHeader.SetMode)
- [func (h *FileHeader) ModTime() time.Time](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#FileHeader.ModTime)
- [func (h *FileHeader) SetModTime(t time.Time)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#FileHeader.SetModTime)

[type File](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#File)

- [func (f *File) DataOffset() (offset int64, err error)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#File.DataOffset)
- [func (f *File) Open() (rc io.ReadCloser, err error)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#File.Open)

[type Reader](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#Reader)

- [func NewReader(r io.ReaderAt, size int64) (*Reader, error)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#NewReader)

[type ReadCloser](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#ReadCloser)

- [func OpenReader(name string) (*ReadCloser, error)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#OpenReader)
- [func (rc *ReadCloser) Close() error](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#ReadCloser.Close)

[type Writer](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#Writer)

- [func NewWriter(w io.Writer) *Writer](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#NewWriter)
- [func (w *Writer) CreateHeader(fh *FileHeader) (io.Writer, error)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#Writer.CreateHeader)
- [func (w *Writer) Create(name string) (io.Writer, error)](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#Writer.Create)
- [func (w *Writer) Close() error](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#Writer.Close)

#### Examples

返回首页



[Reader](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#example-Reader)

[Writer](https://studygolang.com/static/pkgdoc/pkg/archive_zip.htm#example-Writer)

### Constants

```go
const (
    Store   uint16 = 0
    Deflate uint16 = 8
)
```

预定义压缩算法。

### Variables

```go
var (
    ErrFormat    = errors.New("zip: not a valid zip file")
    ErrAlgorithm = errors.New("zip: unsupported compression algorithm")
    ErrChecksum  = errors.New("zip: checksum error")
)
```

### type [Compressor](https://github.com/golang/go/blob/master/src/archive/zip/register.go?name=release#17)

```go
type Compressor func(io.Writer) (io.WriteCloser, error)
```

Compressor函数类型会返回一个io.WriteCloser，该接口会将数据压缩后写入提供的接口。关闭时，应将缓冲中的数据刷新到下层接口中。

### type [Decompressor](https://github.com/golang/go/blob/master/src/archive/zip/register.go?name=release#23)

```gp
type Decompressor func(io.Reader) io.ReadCloser
```

Decompressor函数类型会返回一个io.ReadCloser， 该接口的Read方法会将读取自提供的接口的数据提前解压缩。程序员有责任在读取结束时关闭该io.ReadCloser。

### func [RegisterCompressor](https://github.com/golang/go/blob/master/src/archive/zip/register.go?name=release#90)

```go
func RegisterCompressor(method uint16, comp Compressor)
```

RegisterCompressor使用指定的方法ID注册一个Compressor类型函数。常用的方法Store和Deflate是内建的。

### func [RegisterDecompressor](https://github.com/golang/go/blob/master/src/archive/zip/register.go?name=release#78)

```go
func RegisterDecompressor(method uint16, d Decompressor)
```

RegisterDecompressor使用指定的方法ID注册一个Decompressor类型函数。

### type [FileHeader](https://github.com/golang/go/blob/master/src/archive/zip/struct.go?name=release#70)

```go
type FileHeader struct {
    // Name是文件名，它必须是相对路径，不能以设备或斜杠开始，只接受'/'作为路径分隔符
    Name string
    CreatorVersion     uint16
    ReaderVersion      uint16
    Flags              uint16
    Method             uint16
    ModifiedTime       uint16 // MS-DOS时间
    ModifiedDate       uint16 // MS-DOS日期
    CRC32              uint32
    CompressedSize     uint32 // 已弃用；请使用CompressedSize64
    UncompressedSize   uint32 // 已弃用；请使用UncompressedSize64
    CompressedSize64   uint64
    UncompressedSize64 uint64
    Extra              []byte
    ExternalAttrs      uint32 // 其含义依赖于CreatorVersion
    Comment            string
}
```

FileHeader描述zip文件中的一个文件。参见zip的定义获取细节。

#### func [FileInfoHeader](https://github.com/golang/go/blob/master/src/archive/zip/struct.go?name=release#120)

```go
func FileInfoHeader(fi os.FileInfo) (*FileHeader, error)
```

FileInfoHeader返回一个根据fi填写了部分字段的Header。因为os.FileInfo接口的Name方法只返回它描述的文件的无路径名，有可能需要将返回值的Name字段修改为文件的完整路径名。

#### func (*FileHeader) [FileInfo](https://github.com/golang/go/blob/master/src/archive/zip/struct.go?name=release#94)

```go
func (h *FileHeader) FileInfo() os.FileInfo
```

FileInfo返回一个根据h的信息生成的os.FileInfo。

#### func (*FileHeader) [Mode](https://github.com/golang/go/blob/master/src/archive/zip/struct.go?name=release#209)

```go
func (h *FileHeader) Mode() (mode os.FileMode)
```

Mode返回h的权限和模式位。

#### func (*FileHeader) [SetMode](https://github.com/golang/go/blob/master/src/archive/zip/struct.go?name=release#223)

```go
func (h *FileHeader) SetMode(mode os.FileMode)
```

SetMode修改h的权限和模式位。

#### func (*FileHeader) [ModTime](https://github.com/golang/go/blob/master/src/archive/zip/struct.go?name=release#179)

```go
func (h *FileHeader) ModTime() time.Time
```

返回最近一次修改的UTC时间。（精度2s）

#### func (*FileHeader) [SetModTime](https://github.com/golang/go/blob/master/src/archive/zip/struct.go?name=release#185)

```go
func (h *FileHeader) SetModTime(t time.Time)
```

将ModifiedTime和ModifiedDate字段设置为给定的UTC时间。（精度2s）

### type [File](https://github.com/golang/go/blob/master/src/archive/zip/reader.go?name=release#34)

```go
type File struct {
    FileHeader
    // 内含隐藏或非导出字段
}
```

#### func (*File) [DataOffset](https://github.com/golang/go/blob/master/src/archive/zip/reader.go?name=release#122)

```go
func (f *File) DataOffset() (offset int64, err error)
```

DataOffset返回文件的可能存在的压缩数据相对于zip文件起始的偏移量。大多数调用者应使用Open代替，该方法会主动解压缩数据并验证校验和。

#### func (*File) [Open](https://github.com/golang/go/blob/master/src/archive/zip/reader.go?name=release#132)

```go
func (f *File) Open() (rc io.ReadCloser, err error)
```

Open方法返回一个io.ReadCloser接口，提供读取文件内容的方法。可以同时读取多个文件。

### type [Reader](https://github.com/golang/go/blob/master/src/archive/zip/reader.go?name=release#23)

```go
type Reader struct {
    File    []*File
    Comment string
    // 内含隐藏或非导出字段
}
```

Example

```go
// Open a zip archive for reading.
r, err := zip.OpenReader("testdata/readme.zip")
if err != nil {
    log.Fatal(err)
}
defer r.Close()
// Iterate through the files in the archive,
// printing some of their contents.
for _, f := range r.File {
    fmt.Printf("Contents of %s:\n", f.Name)
    rc, err := f.Open()
    if err != nil {
        log.Fatal(err)
    }
    _, err = io.CopyN(os.Stdout, rc, 68)
    if err != nil {
        log.Fatal(err)
    }
    rc.Close()
    fmt.Println()
}
```

Output:

```go
Contents of README:
This is the source code repository for the Go programming language.
```

#### func [NewReader](https://github.com/golang/go/blob/master/src/archive/zip/reader.go?name=release#67)

```go
func NewReader(r io.ReaderAt, size int64) (*Reader, error)
```

NewReader返回一个从r读取数据的*Reader，r被假设其大小为size字节。

### type [ReadCloser](https://github.com/golang/go/blob/master/src/archive/zip/reader.go?name=release#29)

```go
type ReadCloser struct {
    Reader
    // 内含隐藏或非导出字段
}
```

#### func [OpenReader](https://github.com/golang/go/blob/master/src/archive/zip/reader.go?name=release#46)

```go
func OpenReader(name string) (*ReadCloser, error)
```

OpenReader会打开name指定的zip文件并返回一个*ReadCloser。

#### func (*ReadCloser) [Close](https://github.com/golang/go/blob/master/src/archive/zip/reader.go?name=release#113)

```go
func (rc *ReadCloser) Close() error
```

Close关闭zip文件，使它不能用于I/O。

### type [Writer](https://github.com/golang/go/blob/master/src/archive/zip/writer.go?name=release#20)

```go
type Writer struct {
    // 内含隐藏或非导出字段
}
```

Writer类型实现了zip文件的写入器。

Example

```go
// Create a buffer to write our archive to.
buf := new(bytes.Buffer)
// Create a new zip archive.
w := zip.NewWriter(buf)
// Add some files to the archive.
var files = []struct {
    Name, Body string
}{
    {"readme.txt", "This archive contains some text files."},
    {"gopher.txt", "Gopher names:\nGeorge\nGeoffrey\nGonzo"},
    {"todo.txt", "Get animal handling licence.\nWrite more examples."},
}
for _, file := range files {
    f, err := w.Create(file.Name)
    if err != nil {
        log.Fatal(err)
    }
    _, err = f.Write([]byte(file.Body))
    if err != nil {
        log.Fatal(err)
    }
}
// Make sure to check the error on Close.
err := w.Close()
if err != nil {
    log.Fatal(err)
}
```

#### func [NewWriter](https://github.com/golang/go/blob/master/src/archive/zip/writer.go?name=release#33)

```go
func NewWriter(w io.Writer) *Writer
```

NewWriter创建并返回一个将zip文件写入w的*Writer。

#### func (*Writer) [CreateHeader](https://github.com/golang/go/blob/master/src/archive/zip/writer.go?name=release#183)

```go
func (w *Writer) CreateHeader(fh *FileHeader) (io.Writer, error)
```

使用给出的*FileHeader来作为文件的元数据添加一个文件进zip文件。本方法返回一个io.Writer接口（用于写入新添加文件的内容）。新增文件的内容必须在下一次调用CreateHeader、Create或Close方法之前全部写入。

#### func (*Writer) [Create](https://github.com/golang/go/blob/master/src/archive/zip/writer.go?name=release#170)

```go
func (w *Writer) Create(name string) (io.Writer, error)
```

使用给出的文件名添加一个文件进zip文件。本方法返回一个io.Writer接口（用于写入新添加文件的内容）。文件名必须是相对路径，不能以设备或斜杠开始，只接受'/'作为路径分隔。新增文件的内容必须在下一次调用CreateHeader、Create或Close方法之前全部写入。

#### func (*Writer) [Close](https://github.com/golang/go/blob/master/src/archive/zip/writer.go?name=release#39)

```go
func (w *Writer) Close() error
```

Close方法通过写入中央目录关闭该*Writer。本方法不会也没办法关闭下层的io.Writer接口。

# bufio

## package bufio

```
import "bufio"
```

bufio包实现了有缓冲的I/O。它包装一个io.Reader或io.Writer接口对象，创建另一个也实现了该接口，且同时还提供了缓冲和一些文本I/O的帮助函数的对象。

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#pkg-constants)

[Variables](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#pkg-variables)

[type Reader](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader)

- [func NewReader(rd io.Reader) *Reader](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#NewReader)
- [func NewReaderSize(rd io.Reader, size int) *Reader](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#NewReaderSize)
- [func (b *Reader) Reset(r io.Reader)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.Reset)
- [func (b *Reader) Buffered() int](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.Buffered)
- [func (b *Reader) Peek(n int) ([\]byte, error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.Peek)
- [func (b *Reader) Read(p [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.Read)
- [func (b *Reader) ReadByte() (c byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.ReadByte)
- [func (b *Reader) UnreadByte() error](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.UnreadByte)
- [func (b *Reader) ReadRune() (r rune, size int, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.ReadRune)
- [func (b *Reader) UnreadRune() error](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.UnreadRune)
- [func (b *Reader) ReadLine() (line [\]byte, isPrefix bool, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.ReadLine)
- [func (b *Reader) ReadSlice(delim byte) (line [\]byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.ReadSlice)
- [func (b *Reader) ReadBytes(delim byte) (line [\]byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.ReadBytes)
- [func (b *Reader) ReadString(delim byte) (line string, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.ReadString)
- [func (b *Reader) WriteTo(w io.Writer) (n int64, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Reader.WriteTo)

[type Writer](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer)

- [func NewWriter(w io.Writer) *Writer](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#NewWriter)
- [func NewWriterSize(w io.Writer, size int) *Writer](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#NewWriterSize)
- [func (b *Writer) Reset(w io.Writer)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.Reset)
- [func (b *Writer) Buffered() int](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.Buffered)
- [func (b *Writer) Available() int](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.Available)
- [func (b *Writer) Write(p [\]byte) (nn int, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.Write)
- [func (b *Writer) WriteString(s string) (int, error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.WriteString)
- [func (b *Writer) WriteByte(c byte) error](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.WriteByte)
- [func (b *Writer) WriteRune(r rune) (size int, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.WriteRune)
- [func (b *Writer) Flush() error](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.Flush)
- [func (b *Writer) ReadFrom(r io.Reader) (n int64, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Writer.ReadFrom)

[type ReadWriter](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#ReadWriter)

- [func NewReadWriter(r *Reader, w *Writer) *ReadWriter](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#NewReadWriter)

[type SplitFunc](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#SplitFunc)

[func ScanBytes(data [\]byte, atEOF bool) (advance int, token []byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#ScanBytes)

[func ScanRunes(data [\]byte, atEOF bool) (advance int, token []byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#ScanRunes)

[func ScanWords(data [\]byte, atEOF bool) (advance int, token []byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#ScanWords)

[func ScanLines(data [\]byte, atEOF bool) (advance int, token []byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#ScanLines)

[type Scanner](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Scanner)

- [func NewScanner(r io.Reader) *Scanner](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#NewScanner)
- [func (s *Scanner) Split(split SplitFunc)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Scanner.Split)
- [func (s *Scanner) Scan() bool](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Scanner.Scan)
- [func (s *Scanner) Bytes() [\]byte](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Scanner.Bytes)
- [func (s *Scanner) Text() string](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Scanner.Text)
- [func (s *Scanner) Err() error](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#Scanner.Err)

#### Examples

返回首页



[Scanner (Custom)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#example-Scanner--Custom)

[Scanner (Lines)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#example-Scanner--Lines)

[Scanner (Words)](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#example-Scanner--Words)

[Writer](https://studygolang.com/static/pkgdoc/pkg/bufio.htm#example-Writer)

### Constants

```go
const (
    // 用于缓冲一个token，实际需要的最大token尺寸可能小一些，例如缓冲中需要保存一整行内容
    MaxScanTokenSize = 64 * 1024
)
```

### Variables

```go
var (
    ErrInvalidUnreadByte = errors.New("bufio: invalid use of UnreadByte")
    ErrInvalidUnreadRune = errors.New("bufio: invalid use of UnreadRune")
    ErrBufferFull        = errors.New("bufio: buffer full")
    ErrNegativeCount     = errors.New("bufio: negative count")
)
var (
    ErrTooLong         = errors.New("bufio.Scanner: token too long")
    ErrNegativeAdvance = errors.New("bufio.Scanner: SplitFunc returns negative advance count")
    ErrAdvanceTooFar   = errors.New("bufio.Scanner: SplitFunc returns advance count beyond input")
)
```

会被Scanner类型返回的错误。

### type [Reader](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#31)

```go
type Reader struct {
    // 内含隐藏或非导出字段
}
```

Reader实现了给一个io.Reader接口对象附加缓冲。

#### func [NewReader](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#61)

```go
func NewReader(rd io.Reader) *Reader
```

NewReader创建一个具有默认大小缓冲、从r读取的*Reader。

#### func [NewReaderSize](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#46)

```go
func NewReaderSize(rd io.Reader, size int) *Reader
```

NewReaderSize创建一个具有最少有size尺寸的缓冲、从r读取的*Reader。如果参数r已经是一个具有足够大缓冲的* Reader类型值，会返回r。

#### func (*Reader) [Reset](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#67)

```go
func (b *Reader) Reset(r io.Reader)
```

Reset丢弃缓冲中的数据，清除任何错误，将b重设为其下层从r读取数据。

#### func (*Reader) [Buffered](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#261)

```go
func (b *Reader) Buffered() int
```

Buffered返回缓冲中现有的可读取的字节数。

#### func (*Reader) [Peek](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#123)

```go
func (b *Reader) Peek(n int) ([]byte, error)
```

Peek返回输入流的下n个字节，而不会移动读取位置。返回的[]byte只在下一次调用读取操作前合法。如果Peek返回的切片长度比n小，它也会返会一个错误说明原因。如果n比缓冲尺寸还大，返回的错误将是ErrBufferFull。

#### func (*Reader) [Read](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#153)

```go
func (b *Reader) Read(p []byte) (n int, err error)
```

Read读取数据写入p。本方法返回写入p的字节数。本方法一次调用最多会调用下层Reader接口一次Read方法，因此返回值n可能小于len(p)。读取到达结尾时，返回值n将为0而err将为io.EOF。

#### func (*Reader) [ReadByte](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#193)

```go
func (b *Reader) ReadByte() (c byte, err error)
```

ReadByte读取并返回一个字节。如果没有可用的数据，会返回错误。

#### func (*Reader) [UnreadByte](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#208)

```go
func (b *Reader) UnreadByte() error
```

UnreadByte吐出最近一次读取操作读取的最后一个字节。（只能吐出最后一个，多次调用会出问题）

#### func (*Reader) [ReadRune](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#228)

```go
func (b *Reader) ReadRune() (r rune, size int, err error)
```

ReadRune读取一个utf-8编码的unicode码值，返回该码值、其编码长度和可能的错误。如果utf-8编码非法，读取位置只移动1字节，返回U+FFFD，返回值size为1而err为nil。如果没有可用的数据，会返回错误。

#### func (*Reader) [UnreadRune](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#250)

```go
func (b *Reader) UnreadRune() error
```

UnreadRune吐出最近一次ReadRune调用读取的unicode码值。如果最近一次读取不是调用的ReadRune，会返回错误。（从这点看，UnreadRune比UnreadByte严格很多）

#### func (*Reader) [ReadLine](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#325)

```go
func (b *Reader) ReadLine() (line []byte, isPrefix bool, err error)
```

ReadLine是一个低水平的行数据读取原语。大多数调用者应使用ReadBytes('\n')或ReadString('\n')代替，或者使用Scanner。

ReadLine尝试返回一行数据，不包括行尾标志的字节。如果行太长超过了缓冲，返回值isPrefix会被设为true，并返回行的前面一部分。该行剩下的部分将在之后的调用中返回。返回值isPrefix会在返回该行最后一个片段时才设为false。返回切片是缓冲的子切片，只在下一次读取操作之前有效。ReadLine要么返回一个非nil的line，要么返回一个非nil的err，两个返回值至少一个非nil。

返回的文本不包含行尾的标志字节（"\r\n"或"\n"）。如果输入流结束时没有行尾标志字节，方法不会出错，也不会指出这一情况。在调用ReadLine之后调用UnreadByte会总是吐出最后一个读取的字节（很可能是该行的行尾标志字节），即使该字节不是ReadLine返回值的一部分。

#### func (*Reader) [ReadSlice](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#273)

```go
func (b *Reader) ReadSlice(delim byte) (line []byte, err error)
```

ReadSlice读取直到第一次遇到delim字节，返回缓冲里的包含已读取的数据和delim字节的切片。该返回值只在下一次读取操作之前合法。如果ReadSlice放在在读取到delim之前遇到了错误，它会返回在错误之前读取的数据在缓冲中的切片以及该错误（一般是io.EOF）。如果在读取到delim之前缓冲就被写满了，ReadSlice失败并返回ErrBufferFull。因为ReadSlice的返回值会被下一次I/O操作重写，调用者应尽量使用ReadBytes或ReadString替代本法功法。当且仅当ReadBytes方法返回的切片不以delim结尾时，会返回一个非nil的错误。

#### func (*Reader) [ReadBytes](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#367)

```go
func (b *Reader) ReadBytes(delim byte) (line []byte, err error)
```

ReadBytes读取直到第一次遇到delim字节，返回一个包含已读取的数据和delim字节的切片。如果ReadBytes方法在读取到delim之前遇到了错误，它会返回在错误之前读取的数据以及该错误（一般是io.EOF）。当且仅当ReadBytes方法返回的切片不以delim结尾时，会返回一个非nil的错误。

#### func (*Reader) [ReadString](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#415)

```go
func (b *Reader) ReadString(delim byte) (line string, err error)
```

ReadString读取直到第一次遇到delim字节，返回一个包含已读取的数据和delim字节的字符串。如果ReadString方法在读取到delim之前遇到了错误，它会返回在错误之前读取的数据以及该错误（一般是io.EOF）。当且仅当ReadString方法返回的切片不以delim结尾时，会返回一个非nil的错误。

#### func (*Reader) [WriteTo](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#422)

```go
func (b *Reader) WriteTo(w io.Writer) (n int64, err error)
```

WriteTo方法实现了io.WriterTo接口。

### type [Writer](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#479)

```go
type Writer struct {
    // 内含隐藏或非导出字段
}
```

Writer实现了为io.Writer接口对象提供缓冲。如果在向一个Writer类型值写入时遇到了错误，该对象将不再接受任何数据，且所有写操作都会返回该错误。在说有数据都写入后，调用者有义务调用Flush方法以保证所有的数据都交给了下层的io.Writer。

Example

```go
w := bufio.NewWriter(os.Stdout)
fmt.Fprint(w, "Hello, ")
fmt.Fprint(w, "world!")
w.Flush() // Don't forget to flush!
```

Output:

```go
Hello, world!
```

#### func [NewWriter](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#505)

```go
func NewWriter(w io.Writer) *Writer
```

NewWriter创建一个具有默认大小缓冲、写入w的*Writer。

#### func [NewWriterSize](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#489)

```go
func NewWriterSize(w io.Writer, size int) *Writer
```

NewWriterSize创建一个具有最少有size尺寸的缓冲、写入w的*Writer。如果参数w已经是一个具有足够大缓冲的*Writer类型值，会返回w。

#### func (*Writer) [Reset](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#511)

```go
func (b *Writer) Reset(w io.Writer)
```

Reset丢弃缓冲中的数据，清除任何错误，将b重设为将其输出写入w。

#### func (*Writer) [Buffered](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#550)

```go
func (b *Writer) Buffered() int
```

Buffered返回缓冲中已使用的字节数。

#### func (*Writer) [Available](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#547)

```go
func (b *Writer) Available() int
```

Available返回缓冲中还有多少字节未使用。

#### func (*Writer) [Write](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#556)

```go
func (b *Writer) Write(p []byte) (nn int, err error)
```

Write将p的内容写入缓冲。返回写入的字节数。如果返回值nn < len(p)，还会返回一个错误说明原因。

#### func (*Writer) [WriteString](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#626)

```go
func (b *Writer) WriteString(s string) (int, error)
```

WriteString写入一个字符串。返回写入的字节数。如果返回值nn < len(s)，还会返回一个错误说明原因。

#### func (*Writer) [WriteByte](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#581)

```go
func (b *Writer) WriteByte(c byte) error
```

WriteByte写入单个字节。

#### func (*Writer) [WriteRune](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#595)

```go
func (b *Writer) WriteRune(r rune) (size int, err error)
```

WriteRune写入一个unicode码值（的utf-8编码），返回写入的字节数和可能的错误。

#### func (*Writer) [Flush](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#518)

```go
func (b *Writer) Flush() error
```

Flush方法将缓冲中的数据写入下层的io.Writer接口。

#### func (*Writer) [ReadFrom](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#645)

```go
func (b *Writer) ReadFrom(r io.Reader) (n int64, err error)
```

ReadFrom实现了io.ReaderFrom接口。

### type [ReadWriter](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#690)

```go
type ReadWriter struct {
    *Reader
    *Writer
}
```

ReadWriter类型保管了指向Reader和Writer类型的指针，（因此）实现了io.ReadWriter接口。

#### func [NewReadWriter](https://github.com/golang/go/blob/master/src/bufio/bufio.go?name=release#696)

```go
func NewReadWriter(r *Reader, w *Writer) *ReadWriter
```

NewReadWriter申请创建一个新的、将读写操作分派给r和w 的ReadWriter。

### type [SplitFunc](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#57)

```go
type SplitFunc func(data []byte, atEOF bool) (advance int, token []byte, err error)
```

SplitFunc类型代表用于对输出作词法分析的分割函数。

参数data是尚未处理的数据的一个开始部分的切片，参数atEOF表示是否Reader接口不能提供更多的数据。返回值是解析位置前进的字节数，将要返回给调用者的token切片，以及可能遇到的错误。如果数据不足以（保证）生成一个完整的token，例如需要一整行数据但data里没有换行符，SplitFunc可以返回(0, nil, nil)来告诉Scanner读取更多的数据写入切片然后用从同一位置起始、长度更长的切片再试一次（调用SplitFunc类型函数）。

如果返回值err非nil，扫描将终止并将该错误返回给Scanner的调用者。

除非atEOF为真，永远不会使用空切片data调用SplitFunc类型函数。然而，如果atEOF为真，data却可能是非空的、且包含着未处理的文本。

### func [ScanBytes](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#213)

```go
func ScanBytes(data []byte, atEOF bool) (advance int, token []byte, err error)
```

ScanBytes是用于Scanner类型的分割函数（符合SplitFunc），本函数会将每个字节作为一个token返回。

### func [ScanRunes](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#228)

```go
func ScanRunes(data []byte, atEOF bool) (advance int, token []byte, err error)
```

ScanRunes是用于Scanner类型的分割函数（符合SplitFunc），本函数会将每个utf-8编码的unicode码值作为一个token返回。本函数返回的rune序列和range一个字符串的输出rune序列相同。错误的utf-8编码会翻译为U+FFFD = "\xef\xbf\xbd"，但只会消耗一个字节。调用者无法区分正确编码的rune和错误编码的rune。

### func [ScanWords](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#319)

```go
func ScanWords(data []byte, atEOF bool) (advance int, token []byte, err error)
```

ScanRunes是用于Scanner类型的分割函数（符合SplitFunc），本函数会将空白（参见unicode.IsSpace）分隔的片段（去掉前后空白后）作为一个token返回。本函数永远不会返回空字符串。

### func [ScanLines](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#274)

```go
func ScanLines(data []byte, atEOF bool) (advance int, token []byte, err error)
```

ScanRunes是用于Scanner类型的分割函数（符合SplitFunc），本函数会将每一行文本去掉末尾的换行标记作为一个token返回。返回的行可以是空字符串。换行标记为一个可选的回车后跟一个必选的换行符。最后一行即使没有换行符也会作为一个token返回。

### type [Scanner](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#30)

```go
type Scanner struct {
    // 内含隐藏或非导出字段
}
```

Scanner类型提供了方便的读取数据的接口，如从换行符分隔的文本里读取每一行。

成功调用的Scan方法会逐步提供文件的token，跳过token之间的字节。token由SplitFunc类型的分割函数指定；默认的分割函数会将输入分割为多个行，并去掉行尾的换行标志。本包预定义的分割函数可以将文件分割为行、字节、unicode码值、空白分隔的word。调用者可以定制自己的分割函数。

扫描会在抵达输入流结尾、遇到的第一个I/O错误、token过大不能保存进缓冲时，不可恢复的停止。当扫描停止后，当前读取位置可能会远在最后一个获得的token后面。需要更多对错误管理的控制或token很大，或必须从reader连续扫描的程序，应使用bufio.Reader代替。

Example (Custom)

```go
// An artificial input source.
const input = "1234 5678 1234567901234567890"
scanner := bufio.NewScanner(strings.NewReader(input))
// Create a custom split function by wrapping the existing ScanWords function.
split := func(data []byte, atEOF bool) (advance int, token []byte, err error) {
    advance, token, err = bufio.ScanWords(data, atEOF)
    if err == nil && token != nil {
        _, err = strconv.ParseInt(string(token), 10, 32)
    }
    return
}
// Set the split function for the scanning operation.
scanner.Split(split)
// Validate the input
for scanner.Scan() {
    fmt.Printf("%s\n", scanner.Text())
}
if err := scanner.Err(); err != nil {
    fmt.Printf("Invalid input: %s", err)
}
```

Output:

```go
1234
5678
Invalid input: strconv.ParseInt: parsing "1234567901234567890": value out of range
```

Example (Lines)

```go
scanner := bufio.NewScanner(os.Stdin)
for scanner.Scan() {
    fmt.Println(scanner.Text()) // Println will add back the final '\n'
}
if err := scanner.Err(); err != nil {
    fmt.Fprintln(os.Stderr, "reading standard input:", err)
}
```

Example (Words)

```go
// An artificial input source.
const input = "Now is the winter of our discontent,\nMade glorious summer by this sun of York.\n"
scanner := bufio.NewScanner(strings.NewReader(input))
// Set the split function for the scanning operation.
scanner.Split(bufio.ScanWords)
// Count the words.
count := 0
for scanner.Scan() {
    count++
}
if err := scanner.Err(); err != nil {
    fmt.Fprintln(os.Stderr, "reading input:", err)
}
fmt.Printf("%d\n", count)
```

Output:

```
15
```

#### func [NewScanner](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#74)

```go
func NewScanner(r io.Reader) *Scanner
```

NewScanner创建并返回一个从r读取数据的Scanner，默认的分割函数是ScanLines。

#### func (*Scanner) [Split](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#206)

```go
func (s *Scanner) Split(split SplitFunc)
```

Split设置该Scanner的分割函数。本方法必须在Scan之前调用。

#### func (*Scanner) [Scan](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#110)

```go
func (s *Scanner) Scan() bool
```

Scan方法获取当前位置的token（该token可以通过Bytes或Text方法获得），并让Scanner的扫描位置移动到下一个token。当扫描因为抵达输入流结尾或者遇到错误而停止时，本方法会返回false。在Scan方法返回false后，Err方法将返回扫描时遇到的任何错误；除非是io.EOF，此时Err会返回nil。

#### func (*Scanner) [Bytes](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#94)

```go
func (s *Scanner) Bytes() []byte
```

Bytes方法返回最近一次Scan调用生成的token。底层数组指向的数据可能会被下一次Scan的调用重写。

#### func (*Scanner) [Text](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#100)

```go
func (s *Scanner) Text() string
```

Bytes方法返回最近一次Scan调用生成的token，会申请创建一个字符串保存token并返回该字符串。

#### func (*Scanner) [Err](https://github.com/golang/go/blob/master/src/bufio/scan.go?name=release#84)

```go
func (s *Scanner) Err() error
```

Err返回Scanner遇到的第一个非EOF的错误。

# builtin

## package builtin

```
import "builtin"
```

builtin 包为Go的预声明标识符提供了文档。此处列出的条目其实并不在[builtin](https://studygolang.com/static/pkgdoc/pkg/builtin.htm) 包中，对它们的描述只是为了让 godoc 给该语言的特殊标识符提供文档。

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#pkg-constants)

[type bool](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#bool)

[type byte](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#byte)

[type rune](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#rune)

[type int](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#int)

[type int8](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#int8)

[type int16](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#int16)

[type int32](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#int32)

[type int64](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#int64)

[type uint](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#uint)

[type uint8](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#uint8)

[type uint16](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#uint16)

[type uint32](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#uint32)

[type uint64](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#uint64)

[type float32](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#float32)

[type float64](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#float64)

[type complex64](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#complex64)

[type complex128](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#complex128)

[type uintptr](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#uintptr)

[type string](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#string)

[type error](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#error)

[type Type](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#Type)

[type Type1](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#Type1)

[type IntegerType](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#IntegerType)

[type FloatType](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#FloatType)

[type ComplexType](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#ComplexType)

[func real(c ComplexType) FloatType](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#real)

[func imag(c ComplexType) FloatType](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#imag)

[func complex(r, i FloatType) ComplexType](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#complex)

[func new(Type) *Type](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#new)

[func make(Type, size IntegerType) Type](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#make)

[func cap(v Type) int](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#cap)

[func len(v Type) int](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#len)

[func append(slice [\]Type, elems ...Type) []Type](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#append)

[func copy(dst, src [\]Type) int](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#copy)

[func delete(m map[Type\]Type1, key Type)](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#delete)

[func close(c chan<- Type)](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#close)

[func panic(v interface{})](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#panic)

[func recover() interface{}](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#recover)

[func print(args ...Type)](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#print)

[func println(args ...Type)](https://studygolang.com/static/pkgdoc/pkg/builtin.htm#println)

### Constants

```go
const (
    true  = 0 == 0 // 无类型布尔值
    false = 0 != 0 // 无类型布尔值
)
```

true 和false是两个无类型布尔值。

```go
const iota = 0 // 无类型整数值
```

iota是一个预定义的标识符，代表顺序按行增加的无符号整数，每个const声明单元（被括号括起来）相互独立，分别从0开始。

### type [bool](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#14)

```go
type bool bool
```

布尔类型。

### type [byte](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#88)

```go
type byte byte
```

8位无符号整型，是uint8的别名，二者视为同一类型。

### type [rune](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#92)

```go
type rune rune
```

32位有符号整形，int32的别名，二者视为同一类型。

### type [int](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#75)

```go
type int int
```

至少32位的有符号整形，但和int32/rune并非同一类型。

### type [int8](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#40)

```go
type int8 int8
```

8位有符号整形，范围[-128, 127]。

### type [int16](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#44)

```go
type int16 int16
```

16位有符号整形，范围[-32768, 32767]。

### type [int32](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#48)

```go
type int32 int32
```

32位有符号整形，范围[-2147483648, 2147483647]。

### type [int64](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#52)

```go
type int64 int64
```

64位有符号整形，范围[-9223372036854775808, 9223372036854775807]。

### type [uint](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#79)

```go
type uint uint
```

至少32位的无符号整形，但和uint32不是同一类型。

### type [uint8](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#24)

```go
type uint8 uint8
```

8位无符号整型，范围[0, 255]。

### type [uint16](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#28)

```go
type uint16 uint16
```

16位无符号整型，范围[0, 65535]。

### type [uint32](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#32)

```go
type uint32 uint32
```

32位无符号整型，范围[0, 4294967295]。

### type [uint64](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#36)

```go
type uint64 uint64
```

64位无符号整型，范围[0, 18446744073709551615]。

### type [float32](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#55)

```go
type float32 float32
```

所有IEEE-754 32位浮点数的集合，12位有效数字。

### type [float64](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#58)

```go
type float64 float64
```

所有IEEE-754 64位浮点数的集合，16位有效数字。

### type [complex64](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#62)

```go
type complex64 complex64
```

具有float32 类型实部和虚部的复数类型。

### type [complex128](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#66)

```go
type complex128 complex128
```

具有float64 类型实部和虚部的复数类型。

### type [uintptr](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#83)

```go
type uintptr uintptr
```

可以保存任意指针的位模式的整数类型。

### type [string](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#71)

```go
type string string
```

8位byte序列构成的字符串，约定但不必须是utf-8编码的文本。字符串可以为空但不能是nil，其值不可变。

### type [error](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#254)

```go
type error interface {
    Error() string
}
```

内建error接口类型是约定用于表示错误信息，nil值表示无错误。

### type [Type](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#106)

```go
type Type int
```

在本文档中代表任意一个类型，但同一个声明里只代表同一个类型。

```go
var nil Type // Type必须是指针、通道、函数、接口、映射或切片
```

nil是预定义的标识符，代表指针、通道、函数、接口、映射或切片的零值。

### type [Type1](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#111)

```go
type Type1 int
```

在本文档中代表任意一个类型，但同一个声明里只代表同一个类型，用于代表和Type不同的另一类型。

### type [IntegerType](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#115)

```go
type IntegerType int
```

在本文档中代表一个有符号或无符号的整数类型。

### type [FloatType](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#119)

```go
type FloatType float32
```

在本文档中代表一个浮点数类型。

### type [ComplexType](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#123)

```go
type ComplexType complex64
```

在本文档中代表一个复数类型。

### func [real](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#198)

```go
func real(c ComplexType) FloatType
```

返回复数c的实部。

### func [imag](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#203)

```go
func imag(c ComplexType) FloatType
```

返回复数c的虚部。

### func [complex](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#194)

```go
func complex(r, i FloatType) ComplexType
```

使用实部r和虚部i生成一个复数。

### func [new](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#187)

```go
func new(Type) *Type
```

内建函数new分配内存。其第一个实参为类型，而非值。其返回值为指向该类型的新分配的零值的指针。

### func [make](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#182)

```go
func make(Type, size IntegerType) Type
```

内建函数make分配并初始化一个类型为切片、映射、或通道的对象。其第一个实参为类型，而非值。make的返回类型与其参数相同，而非指向它的指针。其具体结果取决于具体的类型：

```go
切片：size指定了其长度。该切片的容量等于其长度。切片支持第二个整数实参可用来指定不同的容量；
     它必须不小于其长度，因此 make([]int, 0, 10) 会分配一个长度为0，容量为10的切片。
映射：初始分配的创建取决于size，但产生的映射长度为0。size可以省略，这种情况下就会分配一个
     小的起始大小。
通道：通道的缓存根据指定的缓存容量初始化。若 size为零或被省略，该信道即为无缓存的。
```

### func [cap](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#164)

```go
func cap(v Type) int
```

内建函数cap返回 v 的容量，这取决于具体类型：

```go
数组：v中元素的数量，与 len(v) 相同
数组指针：*v中元素的数量，与len(v) 相同
切片：切片的容量（底层数组的长度）；若 v为nil，cap(v) 即为零
信道：按照元素的单元，相应信道缓存的容量；若v为nil，cap(v)即为零
```

### func [len](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#155)

```go
func len(v Type) int
```

内建函数len返回 v 的长度，这取决于具体类型：

```go
数组：v中元素的数量
数组指针：*v中元素的数量（v为nil时panic）
切片、映射：v中元素的数量；若v为nil，len(v)即为零
字符串：v中字节的数量
通道：通道缓存中队列（未读取）元素的数量；若v为 nil，len(v)即为零
```

### func [append](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#134)

```go
func append(slice []Type, elems ...Type) []Type
```

内建函数append将元素追加到切片的末尾。若它有足够的容量，其目标就会重新切片以容纳新的元素。否则，就会分配一个新的基本数组。append返回更新后的切片，因此必须存储追加后的结果。

```go
slice = append(slice, elem1, elem2)
slice = append(slice, anotherSlice...)
```

作为特例，可以向一个字节切片append字符串，如下：

```go
slice = append([]byte("hello "), "world"...)
```

### func [copy](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#141)

```go
func copy(dst, src []Type) int
```

内建函数copy将元素从来源切片复制到目标切片中，也能将字节从字符串复制到字节切片中。copy返回被复制的元素数量，它会是 len(src) 和 len(dst) 中较小的那个。来源和目标的底层内存可以重叠。

### func [delete](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#146)

```go
func delete(m map[Type]Type1, key Type)
```

内建函数delete按照指定的键将元素从映射中删除。若m为nil或无此元素，delete不进行操作。

### func [close](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#213)

```go
func close(c chan<- Type)
```

内建函数close关闭信道，该通道必须为双向的或只发送的。它应当只由发送者执行，而不应由接收者执行，其效果是在最后发送的值被接收后停止该通道。在最后的值从已关闭的信道中被接收后，任何对其的接收操作都会无阻塞的成功。对于已关闭的信道，语句：

```go
x, ok := <-c
```

还会将ok置为false。

### func [panic](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#226)

```go
func panic(v interface{})
```

内建函数panic停止当前Go程的正常执行。当函数F调用panic时，F的正常执行就会立刻停止。F中defer的所有函数先入后出执行后，F返回给其调用者G。G如同F一样行动，层层返回，直到该Go程中所有函数都按相反的顺序停止执行。之后，程序被终止，而错误情况会被报告，包括引发该恐慌的实参值，此终止序列称为恐慌过程。

### func [recover](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#237)

```go
func recover() interface{}
```

内建函数recover允许程序管理恐慌过程中的Go程。在defer的函数中，执行recover调用会取回传至panic调用的错误值，恢复正常执行，停止恐慌过程。若recover在defer的函数之外被调用，它将不会停止恐慌过程序列。在此情况下，或当该Go程不在恐慌过程中时，或提供给panic的实参为nil时，recover就会返回nil。

### func [print](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#243)

```go
func print(args ...Type)
```

内建函数print以特有的方法格式化参数并将结果写入标准错误，用于自举和调试。

### func [println](https://github.com/golang/go/blob/master/src/builtin/builtin.go?name=release#250)

```go
func println(args ...Type)
```

println类似print，但会在参数输出之间添加空格，输出结束后换行。

# bytes

## package bytes

```
import "bytes"
```

bytes包实现了操作[]byte的常用函数。本包的函数和strings包的函数相当类似。

### Index

返回首页

[Constants](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#pkg-constants)

[Variables](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#pkg-variables)

[func Compare(a, b [\]byte) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Compare)

[func Equal(a, b [\]byte) bool](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Equal)

[func EqualFold(s, t [\]byte) bool](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#EqualFold)

[func Runes(s [\]byte) []rune](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Runes)

[func HasPrefix(s, prefix [\]byte) bool](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#HasPrefix)

[func HasSuffix(s, suffix [\]byte) bool](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#HasSuffix)

[func Contains(b, subslice [\]byte) bool](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Contains)

[func Count(s, sep [\]byte) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Count)

[func Index(s, sep [\]byte) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Index)

[func IndexByte(s [\]byte, c byte) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#IndexByte)

[func IndexRune(s [\]byte, r rune) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#IndexRune)

[func IndexAny(s [\]byte, chars string) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#IndexAny)

[func IndexFunc(s [\]byte, f func(r rune) bool) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#IndexFunc)

[func LastIndex(s, sep [\]byte) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#LastIndex)

[func LastIndexAny(s [\]byte, chars string) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#LastIndexAny)

[func LastIndexFunc(s [\]byte, f func(r rune) bool) int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#LastIndexFunc)

[func Title(s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Title)

[func ToLower(s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#ToLower)

[func ToLowerSpecial(_case unicode.SpecialCase, s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#ToLowerSpecial)

[func ToUpper(s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#ToUpper)

[func ToUpperSpecial(_case unicode.SpecialCase, s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#ToUpperSpecial)

[func ToTitle(s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#ToTitle)

[func ToTitleSpecial(_case unicode.SpecialCase, s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#ToTitleSpecial)

[func Repeat(b [\]byte, count int) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Repeat)

[func Replace(s, old, new [\]byte, n int) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Replace)

[func Map(mapping func(r rune) rune, s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Map)

[func Trim(s [\]byte, cutset string) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Trim)

[func TrimSpace(s [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#TrimSpace)

[func TrimFunc(s [\]byte, f func(r rune) bool) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#TrimFunc)

[func TrimLeft(s [\]byte, cutset string) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#TrimLeft)

[func TrimLeftFunc(s [\]byte, f func(r rune) bool) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#TrimLeftFunc)

[func TrimPrefix(s, prefix [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#TrimPrefix)

[func TrimRight(s [\]byte, cutset string) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#TrimRight)

[func TrimRightFunc(s [\]byte, f func(r rune) bool) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#TrimRightFunc)

[func TrimSuffix(s, suffix [\]byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#TrimSuffix)

[func Fields(s [\]byte) [][]byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Fields)

[func FieldsFunc(s [\]byte, f func(rune) bool) [][]byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#FieldsFunc)

[func Split(s, sep [\]byte) [][]byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Split)

[func SplitN(s, sep [\]byte, n int) [][]byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#SplitN)

[func SplitAfter(s, sep [\]byte) [][]byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#SplitAfter)

[func SplitAfterN(s, sep [\]byte, n int) [][]byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#SplitAfterN)

[func Join(s [\][]byte, sep []byte) []byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Join)

[type Reader](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader)

- [func NewReader(b [\]byte) *Reader](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#NewReader)
- [func (r *Reader) Len() int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.Len)
- [func (r *Reader) Read(b [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.Read)
- [func (r *Reader) ReadByte() (b byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.ReadByte)
- [func (r *Reader) UnreadByte() error](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.UnreadByte)
- [func (r *Reader) ReadRune() (ch rune, size int, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.ReadRune)
- [func (r *Reader) UnreadRune() error](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.UnreadRune)
- [func (r *Reader) Seek(offset int64, whence int) (int64, error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.Seek)
- [func (r *Reader) ReadAt(b [\]byte, off int64) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.ReadAt)
- [func (r *Reader) WriteTo(w io.Writer) (n int64, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Reader.WriteTo)

[type Buffer](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer)

- [func NewBuffer(buf [\]byte) *Buffer](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#NewBuffer)
- [func NewBufferString(s string) *Buffer](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#NewBufferString)
- [func (b *Buffer) Reset()](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.Reset)
- [func (b *Buffer) Len() int](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.Len)
- [func (b *Buffer) Bytes() [\]byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.Bytes)
- [func (b *Buffer) String() string](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.String)
- [func (b *Buffer) Truncate(n int)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.Truncate)
- [func (b *Buffer) Grow(n int)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.Grow)
- [func (b *Buffer) Read(p [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.Read)
- [func (b *Buffer) Next(n int) [\]byte](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.Next)
- [func (b *Buffer) ReadByte() (c byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.ReadByte)
- [func (b *Buffer) UnreadByte() error](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.UnreadByte)
- [func (b *Buffer) ReadRune() (r rune, size int, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.ReadRune)
- [func (b *Buffer) UnreadRune() error](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.UnreadRune)
- [func (b *Buffer) ReadBytes(delim byte) (line [\]byte, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.ReadBytes)
- [func (b *Buffer) ReadString(delim byte) (line string, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.ReadString)
- [func (b *Buffer) Write(p [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.Write)
- [func (b *Buffer) WriteString(s string) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.WriteString)
- [func (b *Buffer) WriteByte(c byte) error](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.WriteByte)
- [func (b *Buffer) WriteRune(r rune) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.WriteRune)
- [func (b *Buffer) ReadFrom(r io.Reader) (n int64, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.ReadFrom)
- [func (b *Buffer) WriteTo(w io.Writer) (n int64, err error)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#Buffer.WriteTo)

#### Examples

返回首页

[Buffer](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#example-Buffer)

[Buffer (Reader)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#example-Buffer--Reader)

[Compare](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#example-Compare)

[Compare (Search)](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#example-Compare--Search)

[TrimPrefix](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#example-TrimPrefix)

[TrimSuffix](https://studygolang.com/static/pkgdoc/pkg/bytes.htm#example-TrimSuffix)

### Constants

```go
const MinRead = 512
```

MinRead是被Buffer.ReadFrom传递给Read调用的最小尺寸。只要该Buffer在保存内容之外有最少MinRead字节的余量，其ReadFrom方法就不会增加底层的缓冲。

### Variables

```go
var ErrTooLarge = errors.New("bytes.Buffer: too large")
```

如果内存中不能申请足够保存数据的缓冲，ErrTooLarge就会被传递给panic函数。

### func [Compare](https://github.com/golang/go/blob/master/src/bytes/bytes_decl.go?name=release#24)

```go
func Compare(a, b []byte) int
```

Compare函数返回一个整数表示两个[]byte切片按字典序比较的结果（类同C的strcmp）。如果a==b返回0；如果a<b返回-1；否则返回+1。nil参数视为空切片。

Example

```go
// Interpret Compare's result by comparing it to zero.
var a, b []byte
if bytes.Compare(a, b) < 0 {
    // a less b
}
if bytes.Compare(a, b) <= 0 {
    // a less or equal b
}
if bytes.Compare(a, b) > 0 {
    // a greater b
}
if bytes.Compare(a, b) >= 0 {
    // a greater or equal b
}
// Prefer Equal to Compare for equality comparisons.
if bytes.Equal(a, b) {
    // a equal b
}
if !bytes.Equal(a, b) {
    // a not equal b
}
```

Example (Search)

```go
// Binary search to find a matching byte slice.
var needle []byte
var haystack [][]byte // Assume sorted
i := sort.Search(len(haystack), func(i int) bool {
    // Return haystack[i] >= needle.
    return bytes.Compare(haystack[i], needle) >= 0
})
if i < len(haystack) && bytes.Equal(haystack[i], needle) {
    // Found it!
}
```

### func [Equal](https://github.com/golang/go/blob/master/src/bytes/bytes_decl.go?name=release#17)

```go
func Equal(a, b []byte) bool
```

判断两个切片的内容是否完全相同。

### func [EqualFold](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#646)

```go
func EqualFold(s, t []byte) bool
```

判断两个utf-8编码切片（将unicode大写、小写、标题三种格式字符视为相同）是否相同。

### func [Runes](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#593)

```go
func Runes(s []byte) []rune
```

Runes函数返回和s等价的[]rune切片。（将utf-8编码的unicode码值分别写入单个rune）

### func [HasPrefix](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#331)

```go
func HasPrefix(s, prefix []byte) bool
```

判断s是否有前缀切片prefix。

### func [HasSuffix](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#336)

```go
func HasSuffix(s, suffix []byte) bool
```

判断s是否有后缀切片suffix。

### func [Contains](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#81)

```go
func Contains(b, subslice []byte) bool
```

判断切片b是否包含子切片subslice。

### func [Count](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#50)

```go
func Count(s, sep []byte) int
```

Count计算s中有多少个不重叠的sep子切片。

### func [Index](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#86)

```go
func Index(s, sep []byte) int
```

子切片sep在s中第一次出现的位置，不存在则返回-1。

### func [IndexByte](https://github.com/golang/go/blob/master/src/bytes/bytes_decl.go?name=release#10)

```go
func IndexByte(s []byte, c byte) int
```

字符c在s中第一次出现的位置，不存在则返回-1。

### func [IndexRune](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#143)

```go
func IndexRune(s []byte, r rune) int
```

unicode字符r的utf-8编码在s中第一次出现的位置，不存在则返回-1。

### func [IndexAny](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#158)

```go
func IndexAny(s []byte, chars string) int
```

字符串chars中的任一utf-8编码在s中第一次出现的位置，如不存在或者chars为空字符串则返回-1

### func [IndexFunc](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#510)

```go
func IndexFunc(s []byte, f func(r rune) bool) int
```

s中第一个满足函数f的位置i（该处的utf-8码值r满足f(r)==true），不存在则返回-1

### func [LastIndex](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#126)

```go
func LastIndex(s, sep []byte) int
```

切片sep在字符串s中最后一次出现的位置，不存在则返回-1。

### func [LastIndexAny](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#183)

```go
func LastIndexAny(s []byte, chars string) int
```

字符串chars中的任一utf-8字符在s中最后一次出现的位置，如不存在或者chars为空字符串则返回-1。

### func [LastIndexFunc](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#517)

```go
func LastIndexFunc(s []byte, f func(r rune) bool) int
```

s中最后一个满足函数f的unicode码值的位置i，不存在则返回-1。

### func [Title](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#443)

```go
func Title(s []byte) []byte
```

返回s中每个单词的首字母都改为标题格式的拷贝。

BUG: Title用于划分单词的规则不能很好的处理Unicode标点符号。

### func [ToLower](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#391)

```go
func ToLower(s []byte) []byte
```

返回将所有字母都转为对应的小写版本的拷贝。

### func [ToLowerSpecial](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#404)

```go
func ToLowerSpecial(_case unicode.SpecialCase, s []byte) []byte
```

使用_case规定的字符映射，返回将所有字母都转为对应的小写版本的拷贝。

### func [ToUpper](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#388)

```go
func ToUpper(s []byte) []byte
```

返回将所有字母都转为对应的大写版本的拷贝。

### func [ToUpperSpecial](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#398)

```go
func ToUpperSpecial(_case unicode.SpecialCase, s []byte) []byte
```

使用_case规定的字符映射，返回将所有字母都转为对应的大写版本的拷贝。

### func [ToTitle](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#394)

```go
func ToTitle(s []byte) []byte
```

返回将所有字母都转为对应的标题版本的拷贝。

### func [ToTitleSpecial](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#410)

```go
func ToTitleSpecial(_case unicode.SpecialCase, s []byte) []byte
```

使用_case规定的字符映射，返回将所有字母都转为对应的标题版本的拷贝。

### func [Repeat](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#378)

```go
func Repeat(b []byte, count int) []byte
```

返回count个b串联形成的新的切片。

### func [Replace](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#608)

```go
func Replace(s, old, new []byte, n int) []byte
```

返回将s中前n个不重叠old切片序列都替换为new的新的切片拷贝，如果n<0会替换所有old子切片。

### func [Map](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#344)

```go
func Map(mapping func(r rune) rune, s []byte) []byte
```

将s的每一个unicode码值r都替换为mapping(r)，返回这些新码值组成的切片拷贝。如果mapping返回一个负值，将会丢弃该码值而不会被替换（返回值中对应位置将没有码值）。

### func [Trim](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#570)

```go
func Trim(s []byte, cutset string) []byte
```

返回将s前后端所有cutset包含的unicode码值都去掉的子切片。（共用底层数组）

### func [TrimSpace](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#588)

```go
func TrimSpace(s []byte) []byte
```

返回将s前后端所有空白（unicode.IsSpace指定）都去掉的子切片。（共用底层数组）

### func [TrimFunc](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#485)

```go
func TrimFunc(s []byte, f func(r rune) bool) []byte
```

返回将s前后端所有满足f的unicode码值都去掉的子切片。（共用底层数组）

### func [TrimLeft](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#576)

```go
func TrimLeft(s []byte, cutset string) []byte
```

返回将s前端所有cutset包含的unicode码值都去掉的子切片。（共用底层数组）

### func [TrimLeftFunc](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#462)

```go
func TrimLeftFunc(s []byte, f func(r rune) bool) []byte
```

返回将s前端所有满足f的unicode码值都去掉的子切片。（共用底层数组）

### func [TrimPrefix](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#491)

```go
func TrimPrefix(s, prefix []byte) []byte
```

返回去除s可能的前缀prefix的子切片。（共用底层数组）

Example

```go
var b = []byte("Goodbye,, world!")
b = bytes.TrimPrefix(b, []byte("Goodbye,"))
b = bytes.TrimPrefix(b, []byte("See ya,"))
fmt.Printf("Hello%s", b)
```

Output:

```go
Hello, world!
```

### func [TrimRight](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#582)

```go
func TrimRight(s []byte, cutset string) []byte
```

返回将s后端所有cutset包含的unicode码值都去掉的子切片。（共用底层数组）

### func [TrimRightFunc](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#472)

```go
func TrimRightFunc(s []byte, f func(r rune) bool) []byte
```

返回将s后端所有满足f的unicode码值都去掉的子切片。（共用底层数组）

### func [TrimSuffix](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#500)

```go
func TrimSuffix(s, suffix []byte) []byte
```

返回去除s可能的后缀suffix的子切片。（共用底层数组）

Example

```go
var b = []byte("Hello, goodbye, etc!")
b = bytes.TrimSuffix(b, []byte("goodbye, etc!"))
b = bytes.TrimSuffix(b, []byte("gopher"))
b = append(b, bytes.TrimSuffix([]byte("world!"), []byte("x!"))...)
os.Stdout.Write(b)
```

Output:

```go
Hello, world!
```

### func [Fields](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#262)

```go
func Fields(s []byte) [][]byte
```

返回将字符串按照空白（unicode.IsSpace确定，可以是一到多个连续的空白字符）分割的多个子切片。如果字符串全部是空白或者是空字符串的话，会返回空切片。

### func [FieldsFunc](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#270)

```go
func FieldsFunc(s []byte, f func(rune) bool) [][]byte
```

类似Fields，但使用函数f来确定分割符（满足f的utf-8码值）。如果字符串全部是分隔符或者是空字符串的话，会返回空切片。

### func [Split](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#250)

```go
func Split(s, sep []byte) [][]byte
```

用去掉s中出现的sep的方式进行分割，会分割到结尾，并返回生成的所有[]byte切片组成的切片（每一个sep都会进行一次切割，即使两个sep相邻，也会进行两次切割）。如果sep为空字符，Split会将s切分成每一个unicode码值一个[]byte切片。

### func [SplitN](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#233)

```go
func SplitN(s, sep []byte, n int) [][]byte
```

用去掉s中出现的sep的方式进行分割，会分割到最多n个子切片，并返回生成的所有[]byte切片组成的切片（每一个sep都会进行一次切割，即使两个sep相邻，也会进行两次切割）。如果sep为空字符，Split会将s切分成每一个unicode码值一个[]byte切片。参数n决定返回的切片的数目：

```go
n > 0 : 返回的切片最多n个子字符串；最后一个子字符串包含未进行切割的部分。
n == 0: 返回nil
n < 0 : 返回所有的子字符串组成的切片
```

### func [SplitAfter](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#256)

```go
func SplitAfter(s, sep []byte) [][]byte
```

用从s中出现的sep后面切断的方式进行分割，会分割到结尾，并返回生成的所有[]byte切片组成的切片（每一个sep都会进行一次切割，即使两个sep相邻，也会进行两次切割）。如果sep为空字符，Split会将s切分成每一个unicode码值一个[]byte切片。

### func [SplitAfterN](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#242)

```go
func SplitAfterN(s, sep []byte, n int) [][]byte
```

用从s中出现的sep后面切断的方式进行分割，会分割到最多n个子切片，并返回生成的所有[]byte切片组成的切片（每一个sep都会进行一次切割，即使两个sep相邻，也会进行两次切割）。如果sep为空字符，Split会将s切分成每一个unicode码值一个[]byte切片。参数n决定返回的切片的数目：

```go
n > 0 : 返回的切片最多n个子字符串；最后一个子字符串包含未进行切割的部分。
n == 0: 返回nil
n < 0 : 返回所有的子字符串组成的切片
```

### func [Join](https://github.com/golang/go/blob/master/src/bytes/bytes.go?name=release#308)

```go
func Join(s [][]byte, sep []byte) []byte
```

将一系列[]byte切片连接为一个[]byte切片，之间用sep来分隔，返回生成的新切片。

### type [Reader](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#17)

```go
type Reader struct {
    // 内含隐藏或非导出字段
}
```

Reader类型通过从一个[]byte读取数据，实现了io.Reader、io.Seeker、io.ReaderAt、io.WriterTo、io.ByteScanner、io.RuneScanner接口。

#### func [NewReader](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#144)

```go
func NewReader(b []byte) *Reader
```

NewReader创建一个从s读取数据的Reader。

#### func (*Reader) [Len](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#25)

```go
func (r *Reader) Len() int
```

Len返回r包含的切片中还没有被读取的部分。

#### func (*Reader) [Read](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#32)

```go
func (r *Reader) Read(b []byte) (n int, err error)
```

#### func (*Reader) [ReadByte](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#60)

```go
func (r *Reader) ReadByte() (b byte, err error)
```

#### func (*Reader) [UnreadByte](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#70)

```go
func (r *Reader) UnreadByte() error
```

#### func (*Reader) [ReadRune](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#79)

```go
func (r *Reader) ReadRune() (ch rune, size int, err error)
```

#### func (*Reader) [UnreadRune](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#94)

```go
func (r *Reader) UnreadRune() error
```

#### func (*Reader) [Seek](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#104)

```go
func (r *Reader) Seek(offset int64, whence int) (int64, error)
```

Seek实现了io.Seeker接口。

#### func (*Reader) [ReadAt](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#45)

```go
func (r *Reader) ReadAt(b []byte, off int64) (n int, err error)
```

#### func (*Reader) [WriteTo](https://github.com/golang/go/blob/master/src/bytes/reader.go?name=release#125)

```go
func (r *Reader) WriteTo(w io.Writer) (n int64, err error)
```

WriteTo实现了io.WriterTo接口。

### type [Buffer](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#17)

```go
type Buffer struct {
    // 内含隐藏或非导出字段
}
```

Buffer是一个实现了读写方法的可变大小的字节缓冲。本类型的零值是一个空的可用于读写的缓冲。

Example

```go
var b bytes.Buffer // A Buffer needs no initialization.
b.Write([]byte("Hello "))
fmt.Fprintf(&b, "world!")
b.WriteTo(os.Stdout)
```

Output:

```go
Hello world!
```

Example (Reader)

```go
// A Buffer can turn a string or a []byte into an io.Reader.
buf := bytes.NewBufferString("R29waGVycyBydWxlIQ==")
dec := base64.NewDecoder(base64.StdEncoding, buf)
io.Copy(os.Stdout, dec)
```

Output:

```go
Gophers rule!
```

#### func [NewBuffer](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#402)

```go
func NewBuffer(buf []byte) *Buffer
```

NewBuffer使用buf作为初始内容创建并初始化一个Buffer。本函数用于创建一个用于读取已存在数据的buffer；也用于指定用于写入的内部缓冲的大小，此时，buf应为一个具有指定容量但长度为0的切片。buf会被作为返回值的底层缓冲切片。

大多数情况下，new(Buffer)（或只是声明一个Buffer类型变量）就足以初始化一个Buffer了。

#### func [NewBufferString](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#410)

```go
func NewBufferString(s string) *Buffer
```

NewBuffer使用s作为初始内容创建并初始化一个Buffer。本函数用于创建一个用于读取已存在数据的buffer。

大多数情况下，new(Buffer)（或只是声明一个Buffer类型变量）就足以初始化一个Buffer了。

#### func (*Buffer) [Reset](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#75)

```go
func (b *Buffer) Reset()
```

Reset重设缓冲，因此会丢弃全部内容，等价于b.Truncate(0)。

#### func (*Buffer) [Len](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#57)

```go
func (b *Buffer) Len() int
```

返回缓冲中未读取部分的字节长度；b.Len() == len(b.Bytes())。

#### func (*Buffer) [Bytes](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#43)

```go
func (b *Buffer) Bytes() []byte
```

返回未读取部分字节数据的切片，len(b.Bytes()) == b.Len()。如果中间没有调用其他方法，修改返回的切片的内容会直接改变Buffer的内容。

#### func (*Buffer) [String](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#47)

```go
func (b *Buffer) String() string
```

将未读取部分的字节数据作为字符串返回，如果b是nil指针，会返回"<nil>"。

#### func (*Buffer) [Truncate](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#61)

```go
func (b *Buffer) Truncate(n int)
```

丢弃缓冲中除前n字节数据外的其它数据，如果n小于零或者大于缓冲容量将panic。

#### func (*Buffer) [Grow](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#114)

```go
func (b *Buffer) Grow(n int)
```

必要时会增加缓冲的容量，以保证n字节的剩余空间。调用Grow(n)后至少可以向缓冲中写入n字节数据而无需申请内存。如果n小于零或者不能增加容量都会panic。

#### func (*Buffer) [Read](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#251)

```go
func (b *Buffer) Read(p []byte) (n int, err error)
```

Read方法从缓冲中读取数据直到缓冲中没有数据或者读取了len(p)字节数据，将读取的数据写入p。返回值n是读取的字节数，除非缓冲中完全没有数据可以读取并写入p，此时返回值err为io.EOF；否则err总是nil。

#### func (*Buffer) [Next](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#273)

```go
func (b *Buffer) Next(n int) []byte
```

返回未读取部分前n字节数据的切片，并且移动读取位置，就像调用了Read方法一样。如果缓冲内数据不足，会返回整个数据的切片。切片只在下一次调用b的读/写方法前才合法。

#### func (*Buffer) [ReadByte](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#289)

```go
func (b *Buffer) ReadByte() (c byte, err error)
```

ReadByte读取并返回缓冲中的下一个字节。如果没有数据可用，返回值err为io.EOF。

#### func (*Buffer) [UnreadByte](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#345)

```go
func (b *Buffer) UnreadByte() error
```

UnreadByte吐出最近一次读取操作读取的最后一个字节。如果最后一次读取操作之后进行了写入，本方法会返回错误。

#### func (*Buffer) [ReadRune](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#307)

```go
func (b *Buffer) ReadRune() (r rune, size int, err error)
```

ReadRune读取并返回缓冲中的下一个utf-8码值。如果没有数据可用，返回值err为io.EOF。如果缓冲中的数据是错误的utf-8编码，本方法会吃掉一字节并返回(U+FFFD, 1, nil)。

#### func (*Buffer) [UnreadRune](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#330)

```go
func (b *Buffer) UnreadRune() error
```

UnreadRune吐出最近一次调用ReadRune方法读取的unicode码值。如果最近一次读写操作不是ReadRune，本方法会返回错误。（这里就能看出来UnreadRune比UnreadByte严格多了）

#### func (*Buffer) [ReadBytes](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#362)

```go
func (b *Buffer) ReadBytes(delim byte) (line []byte, err error)
```

ReadBytes读取直到第一次遇到delim字节，返回一个包含已读取的数据和delim字节的切片。如果ReadBytes方法在读取到delim之前遇到了错误，它会返回在错误之前读取的数据以及该错误（一般是io.EOF）。当且仅当ReadBytes方法返回的切片不以delim结尾时，会返回一个非nil的错误。

#### func (*Buffer) [ReadString](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#390)

```go
func (b *Buffer) ReadString(delim byte) (line string, err error)
```

ReadString读取直到第一次遇到delim字节，返回一个包含已读取的数据和delim字节的字符串。如果ReadString方法在读取到delim之前遇到了错误，它会返回在错误之前读取的数据以及该错误（一般是io.EOF）。当且仅当ReadString方法返回的切片不以delim结尾时，会返回一个非nil的错误。

#### func (*Buffer) [Write](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#125)

```go
func (b *Buffer) Write(p []byte) (n int, err error)
```

Write将p的内容写入缓冲中，如必要会增加缓冲容量。返回值n为len(p)，err总是nil。如果缓冲变得太大，Write会采用错误值ErrTooLarge引发panic。

#### func (*Buffer) [WriteString](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#134)

```go
func (b *Buffer) WriteString(s string) (n int, err error)
```

Write将s的内容写入缓冲中，如必要会增加缓冲容量。返回值n为len(p)，err总是nil。如果缓冲变得太大，Write会采用错误值ErrTooLarge引发panic。

#### func (*Buffer) [WriteByte](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#226)

```go
func (b *Buffer) WriteByte(c byte) error
```

WriteByte将字节c写入缓冲中，如必要会增加缓冲容量。返回值总是nil，但仍保留以匹配bufio.Writer的WriteByte方法。如果缓冲太大，WriteByte会采用错误值ErrTooLarge引发panic。

#### func (*Buffer) [WriteRune](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#237)

```go
func (b *Buffer) WriteRune(r rune) (n int, err error)
```

WriteByte将unicode码值r的utf-8编码写入缓冲中，如必要会增加缓冲容量。返回值总是nil，但仍保留以匹配bufio.Writer的WriteRune方法。如果缓冲太大，WriteRune会采用错误值ErrTooLarge引发panic。

#### func (*Buffer) [ReadFrom](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#150)

```go
func (b *Buffer) ReadFrom(r io.Reader) (n int64, err error)
```

ReadFrom从r中读取数据直到结束并将读取的数据写入缓冲中，如必要会增加缓冲容量。返回值n为从r读取并写入b的字节数；会返回读取时遇到的除了io.EOF之外的错误。如果缓冲太大，ReadFrom会采用错误值ErrTooLarge引发panic。

#### func (*Buffer) [WriteTo](https://github.com/golang/go/blob/master/src/bytes/buffer.go?name=release#198)

```go
func (b *Buffer) WriteTo(w io.Writer) (n int64, err error)
```

WriteTo从缓冲中读取数据直到缓冲内没有数据或遇到错误，并将这些数据写入w。返回值n为从b读取并写入w的字节数；返回值总是可以无溢出的写入int类型，但为了匹配io.WriterTo接口设为int64类型。从b读取是遇到的非io.EOF错误及写入w时遇到的错误都会终止本方法并返回该错误。

# compress/bzip2

## package bzip2

```
import "compress/bzip2"
```

bzip2包实现bzip2的解压缩。

### Index

返回首页



[type StructuralError](https://studygolang.com/static/pkgdoc/pkg/compress_bzip2.htm#StructuralError)

- [func (s StructuralError) Error() string](https://studygolang.com/static/pkgdoc/pkg/compress_bzip2.htm#StructuralError.Error)

[func NewReader(r io.Reader) io.Reader](https://studygolang.com/static/pkgdoc/pkg/compress_bzip2.htm#NewReader)

### type [StructuralError](https://github.com/golang/go/blob/master/src/compress/bzip2/bzip2.go?name=release#17)

```go
type StructuralError string
```

当bzip2数据的语法不合法时，会返回本类型错误。

#### func (StructuralError) [Error](https://github.com/golang/go/blob/master/src/compress/bzip2/bzip2.go?name=release#19)

```go
func (s StructuralError) Error() string
```

### func [NewReader](https://github.com/golang/go/blob/master/src/compress/bzip2/bzip2.go?name=release#45)

```go
func NewReader(r io.Reader) io.Reader
```

NewReader返回一个从r读取bzip2压缩数据并解压缩后返回给调用者的io.Reader。

# compress/flate

## package flate

```go
import "compress/flate"
```

flate包实现了deflate压缩数据格式，参见[RFC 1951](http://tools.ietf.org/html/rfc1951)。gzip包和zlib包实现了对基于deflate的文件格式的访问。

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#pkg-constants)

[type CorruptInputError](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#CorruptInputError)

- [func (e CorruptInputError) Error() string](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#CorruptInputError.Error)

[type InternalError](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#InternalError)

- [func (e InternalError) Error() string](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#InternalError.Error)

[type ReadError](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#ReadError)

- [func (e *ReadError) Error() string](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#ReadError.Error)

[type WriteError](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#WriteError)

- [func (e *WriteError) Error() string](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#WriteError.Error)

[type Reader](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#Reader)

- [func NewReader(r io.Reader) io.ReadCloser](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#NewReader)
- [func NewReaderDict(r io.Reader, dict [\]byte) io.ReadCloser](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#NewReaderDict)

[type Writer](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#Writer)

- [func NewWriter(w io.Writer, level int) (*Writer, error)](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#NewWriter)
- [func NewWriterDict(w io.Writer, level int, dict [\]byte) (*Writer, error)](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#NewWriterDict)
- [func (w *Writer) Reset(dst io.Writer)](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#Writer.Reset)
- [func (w *Writer) Write(data [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#Writer.Write)
- [func (w *Writer) Flush() error](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#Writer.Flush)
- [func (w *Writer) Close() error](https://studygolang.com/static/pkgdoc/pkg/compress_flate.htm#Writer.Close)

### Constants

```go
const (
    NoCompression = 0
    BestSpeed     = 1
    BestCompression    = 9
    DefaultCompression = -1
)
```

### type [CorruptInputError](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#26)

```go
type CorruptInputError int64
```

CorruptInputError表示在输入的指定偏移量位置存在损坏。

#### func (CorruptInputError) [Error](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#28)

```go
func (e CorruptInputError) Error() string
```

### type [InternalError](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#33)

```go
type InternalError string
```

InternalError表示flate数据自身的错误。

#### func (InternalError) [Error](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#35)

```go
func (e InternalError) Error() string
```

### type [ReadError](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#38)

```go
type ReadError struct {
    Offset int64 // 错误出现的位置（字节偏移量）
    Err    error // 下层的读取操作返回的错误
}
```

ReadError代表在读取输入流时遇到的错误。

#### func (*ReadError) [Error](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#43)

```go
func (e *ReadError) Error() string
```

### type [WriteError](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#48)

```go
type WriteError struct {
    Offset int64 // 错误出现的位置（字节偏移量）
    Err    error // 下层的写入操作返回的错误
}
```

WriteError代表在写入输出流时遇到的错误。

#### func (*WriteError) [Error](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#53)

```go
func (e *WriteError) Error() string
```

### type [Reader](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#181)

```go
type Reader interface {
    io.Reader
    io.ByteReader
}
```

NewReader真正需要的接口。如果提供的Io.Reader没有提供ReadByte方法，NewReader函数会自行添加缓冲。

#### func [NewReader](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#684)

```go
func NewReader(r io.Reader) io.ReadCloser
```

NewReader返回一个从r读取并解压数据的io.ReadCloser。调用者有责任在读取完毕后调用返回值的Close方法。

#### func [NewReaderDict](https://github.com/golang/go/blob/master/src/compress/flate/inflate.go?name=release#699)

```go
func NewReaderDict(r io.Reader, dict []byte) io.ReadCloser
```

NewReaderDict类似NewReader，但会使用预设的字典初始化返回的Reader。

返回的Reader表现的好像原始未压缩的数据流以该字典起始（并已经被读取）。NewReaderDict用于读取NewWriterDict压缩的数据。

### type [Writer](https://github.com/golang/go/blob/master/src/compress/flate/deflate.go?name=release#526)

```go
type Writer struct {
    // 内含隐藏或非导出字段
}
```

Writer将提供给它的数据压缩后写入下层的io.Writer接口。

#### func [NewWriter](https://github.com/golang/go/blob/master/src/compress/flate/deflate.go?name=release#485)

```go
func NewWriter(w io.Writer, level int) (*Writer, error)
```

NewWriter返回一个压缩水平为level的Writer。

和zlib包一样，level的范围是1（BestSpeed）到9 （BestCompression）。值越大，压缩效果越好，但也越慢；level为0表示不尝试做任何压缩，只添加必需的deflate框架；level为-1时会使用默认的压缩水平；如果level在[-1, 9]范围内，error返回值将是nil，否则将返回非nil的错误值。

#### func [NewWriterDict](https://github.com/golang/go/blob/master/src/compress/flate/deflate.go?name=release#499)

```go
func NewWriterDict(w io.Writer, level int, dict []byte) (*Writer, error)
```

NewWriterDict类似NewWriter，但会使用预设的字典初始化返回的Writer。

返回的Writer表现的好像已经将原始、未压缩数据dict（压缩后未产生任何数据的）写入w了，使用w压缩的数据只能被使用同样的字典初始化生成的Reader接口解压缩。（类似加解密的初始向量/密钥）

#### func (*Writer) [Reset](https://github.com/golang/go/blob/master/src/compress/flate/deflate.go?name=release#558)

```go
func (w *Writer) Reset(dst io.Writer)
```

Reset将w重置，丢弃当前的写入状态，并将下层输出目标设为dst。效果上等价于将w设为使用dst和w的压缩水平、字典重新调用NewWriter或NewWriterDict返回的*Writer。

#### func (*Writer) [Write](https://github.com/golang/go/blob/master/src/compress/flate/deflate.go?name=release#533)

```go
func (w *Writer) Write(data []byte) (n int, err error)
```

Write向w写入数据，最终会将压缩后的数据写入下层io.Writer接口。

#### func (*Writer) [Flush](https://github.com/golang/go/blob/master/src/compress/flate/deflate.go?name=release#544)

```go
func (w *Writer) Flush() error
```

Flush将缓冲中的压缩数据刷新到下层io.Writer接口中。

本方法主要用在传输压缩数据的网络连接中，以保证远端的接收者可以获得足够的数据来重构数据报。Flush会阻塞直到所有缓冲中的数据都写入下层io.Writer接口后才返回。如果下层的io.Writetr接口返回一个错误，Flush也会返回该错误。在zlib包的术语中，Flush方法等价于Z_SYNC_FLUSH。

#### func (*Writer) [Close](https://github.com/golang/go/blob/master/src/compress/flate/deflate.go?name=release#551)

```go
func (w *Writer) Close() error
```

Close刷新缓冲并关闭w。

# compress/gzip

## package gzip

```go
import "compress/gzip"
```

gzip包实现了gzip格式压缩文件的读写，参见[RFC 1952](http://tools.ietf.org/html/rfc1952)。

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#pkg-constants)

[Variables](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#pkg-variables)

[type Header](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Header)

[type Reader](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Reader)

- [func NewReader(r io.Reader) (*Reader, error)](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#NewReader)
- [func (z *Reader) Reset(r io.Reader) error](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Reader.Reset)
- [func (z *Reader) Read(p [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Reader.Read)
- [func (z *Reader) Close() error](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Reader.Close)

[type Writer](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Writer)

- [func NewWriter(w io.Writer) *Writer](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#NewWriter)
- [func NewWriterLevel(w io.Writer, level int) (*Writer, error)](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#NewWriterLevel)
- [func (z *Writer) Reset(w io.Writer)](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Writer.Reset)
- [func (z *Writer) Write(p [\]byte) (int, error)](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Writer.Write)
- [func (z *Writer) Flush() error](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Writer.Flush)
- [func (z *Writer) Close() error](https://studygolang.com/static/pkgdoc/pkg/compress_gzip.htm#Writer.Close)

### Constants

```go
const (
    NoCompression      = flate.NoCompression
    BestSpeed          = flate.BestSpeed
    BestCompression    = flate.BestCompression
    DefaultCompression = flate.DefaultCompression
)
```

这些常量都是拷贝自flate包，因此导入"compress/gzip"后，就不必再导入"compress/flate"了。

### Variables

```go
var (
    // 当读取的gzip数据的校验和错误时，会返回ErrChecksum
    ErrChecksum = errors.New("gzip: invalid checksum")
    // 当读取的gzip数据的头域错误时，会返回ErrHeader
    ErrHeader = errors.New("gzip: invalid header")
)
```

### type [Header](https://github.com/golang/go/blob/master/src/compress/gzip/gunzip.go?name=release#46)

```go
type Header struct {
    Comment string    // 注释
    Extra   []byte    // 额外数据
    ModTime time.Time // 修改时间
    Name    string    // 文件名
    OS      byte      // 操作系统类型
}
```

gzip文件保存一个头域，提供关于被压缩的文件的一些元数据。该头域作为Writer和Reader类型的一个可导出字段，可以提供给调用者访问。

### type [Reader](https://github.com/golang/go/blob/master/src/compress/gzip/gunzip.go?name=release#68)

```go
type Reader struct {
    Header
    // 内含隐藏或非导出字段
}
```

Reader类型满足io.Reader接口，可以从gzip格式压缩文件读取并解压数据。

一般，一个gzip文件可以是多个gzip文件的串联，每一个都有自己的头域。从Reader读取数据会返回串联的每个文件的解压数据，但只有第一个文件的头域被记录在Reader的Header字段里。

gzip文件会保存未压缩数据的长度与校验和。当读取到未压缩数据的结尾时，如果数据的长度或者校验和不正确，Reader会返回ErrCheckSum。因此，调用者应该将Read方法返回的数据视为暂定的，直到他们在数据结尾获得了一个io.EOF。

#### func [NewReader](https://github.com/golang/go/blob/master/src/compress/gzip/gunzip.go?name=release#82)

```go
func NewReader(r io.Reader) (*Reader, error)
```

NewReader返回一个从r读取并解压数据的*Reader。其实现会缓冲输入流的数据，并可能从r中读取比需要的更多的数据。调用者有责任在读取完毕后调用返回值的Close方法。

#### func (*Reader) [Reset](https://github.com/golang/go/blob/master/src/compress/gzip/gunzip.go?name=release#95)

```go
func (z *Reader) Reset(r io.Reader) error
```

Reset将z重置，丢弃当前的读取状态，并将下层读取目标设为r。效果上等价于将z设为使用r重新调用NewReader返回的Reader。这让我们可以重用z而不是再申请一个新的。（因此效率更高）

#### func (*Reader) [Read](https://github.com/golang/go/blob/master/src/compress/gzip/gunzip.go?name=release#214)

```go
func (z *Reader) Read(p []byte) (n int, err error)
```

#### func (*Reader) [Close](https://github.com/golang/go/blob/master/src/compress/gzip/gunzip.go?name=release#255)

```go
func (z *Reader) Close() error
```

调用Close会关闭z，但不会关闭下层io.Reader接口。

### type [Writer](https://github.com/golang/go/blob/master/src/compress/gzip/gzip.go?name=release#27)

```go
type Writer struct {
    Header
    // 内含隐藏或非导出字段
}
```

Writer满足io.WriteCloser接口。它会将提供给它的数据压缩后写入下层io.Writer接口。

#### func [NewWriter](https://github.com/golang/go/blob/master/src/compress/gzip/gzip.go?name=release#51)

```go
func NewWriter(w io.Writer) *Writer
```

NewWriter创建并返回一个Writer。写入返回值的数据都会在压缩后写入w。调用者有责任在结束写入后调用返回值的Close方法。因为写入的数据可能保存在缓冲中没有刷新入下层。

如要设定Writer.Header字段，调用者必须在第一次调用Write方法或者Close方法之前设置。Header字段的Comment和Name字段是go的utf-8字符串，但下层格式要求为NUL中止的ISO 8859-1 (Latin-1)序列。如果这两个字段的字符串包含NUL或非Latin-1字符，将导致Write方法返回错误。

#### func [NewWriterLevel](https://github.com/golang/go/blob/master/src/compress/gzip/gzip.go?name=release#62)

```go
func NewWriterLevel(w io.Writer, level int) (*Writer, error)
```

NewWriterLevel类似NewWriter但指定了压缩水平而不是采用默认的DefaultCompression。

参数level可以是DefaultCompression、NoCompression或BestSpeed与BestCompression之间包括二者的任何整数。如果level合法，返回的错误值为nil。

#### func (*Writer) [Reset](https://github.com/golang/go/blob/master/src/compress/gzip/gzip.go?name=release#97)

```go
func (z *Writer) Reset(w io.Writer)
```

Reset将z重置，丢弃当前的写入状态，并将下层输出目标设为dst。效果上等价于将w设为使用dst和w的压缩水平重新调用NewWriterLevel返回的*Writer。这让我们可以重用z而不是再申请一个新的。（因此效率更高）

#### func (*Writer) [Write](https://github.com/golang/go/blob/master/src/compress/gzip/gzip.go?name=release#161)

```go
func (z *Writer) Write(p []byte) (int, error)
```

Write将p压缩后写入下层io.Writer接口。压缩后的数据不一定会立刻刷新，除非Writer被关闭或者显式的刷新。

#### func (*Writer) [Flush](https://github.com/golang/go/blob/master/src/compress/gzip/gzip.go?name=release#231)

```go
func (z *Writer) Flush() error
```

Flush将缓冲中的压缩数据刷新到下层io.Writer接口中。

本方法主要用在传输压缩数据的网络连接中，以保证远端的接收者可以获得足够的数据来重构数据报。Flush会阻塞直到所有缓冲中的数据都写入下层io.Writer接口后才返回。如果下层的io.Writetr接口返回一个错误，Flush也会返回该错误。在zlib包的术语中，Flush方法等价于Z_SYNC_FLUSH。

#### func (*Writer) [Close](https://github.com/golang/go/blob/master/src/compress/gzip/gzip.go?name=release#250)

```go
func (z *Writer) Close() error
```

调用Close会关闭z，但不会关闭下层io.Writer接口。

# compress/lzw

## package lzw

```go
import "compress/lzw"
```

lzw包实现了Lempel-Ziv-Welch数据压缩格式，这是一种T. A. Welch在“A Technique for High-Performance Data Compression”一文（Computer, 17(6) (June 1984), pp 8-19）提出的一种压缩格式。

本包实现了用于GIF、TIFF、PDF文件的lzw压缩格式，这是一种最长达到12位的变长码，头两个非字面码为clear和EOF码。

### Index

返回首页



[type Order](https://studygolang.com/static/pkgdoc/pkg/compress_lzw.htm#Order)

[func NewReader(r io.Reader, order Order, litWidth int) io.ReadCloser](https://studygolang.com/static/pkgdoc/pkg/compress_lzw.htm#NewReader)

[func NewWriter(w io.Writer, order Order, litWidth int) io.WriteCloser](https://studygolang.com/static/pkgdoc/pkg/compress_lzw.htm#NewWriter)

### type [Order](https://github.com/golang/go/blob/master/src/compress/lzw/reader.go?name=release#25)

```go
type Order int
```

Order指定一个lzw数据流的位顺序。

```go
const (
    // LSB表示最小权重位在前，用在GIF文件格式
    LSB Order = iota
    // MSB表示最大权重位在前，用在TIFF和PDF文件格式
    MSB
)
```

### func [NewReader](https://github.com/golang/go/blob/master/src/compress/lzw/reader.go?name=release#225)

```go
func NewReader(r io.Reader, order Order, litWidth int) io.ReadCloser
```

创建一个io.ReadCloser，它从r读取并解压数据。调用者有责任在结束读取后调用返回值的Close方法；litWidth指定字面码的位数，必须在[2,8]范围内，一般为8。

### func [NewWriter](https://github.com/golang/go/blob/master/src/compress/lzw/writer.go?name=release#234)

```go
func NewWriter(w io.Writer, order Order, litWidth int) io.WriteCloser
```

创建一个io.WriteCloser，它将数据压缩后写入w。调用者有责任在结束写入后调用返回值的Close方法；litWidth指定字面码的位数，必须在[2,8]范围内，一般为8。

# compress/zlib

## package zlib

```go
import "compress/zlib"
```

zlib包实现了对zlib格式压缩数据的读写，参见[RFC 1950](http://tools.ietf.org/html/rfc1950)。

本包的实现提供了在读取时解压和写入时压缩的滤镜。例如，将压缩数据写入一个bytes.Buffer：

```go
var b bytes.Buffer
w := zlib.NewWriter(&b)
w.Write([]byte("hello, world\n"))
w.Close()
```

然后将数据读取回来：

```go
r, err := zlib.NewReader(&b)
io.Copy(os.Stdout, r)
r.Close()
```

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#pkg-constants)

[Variables](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#pkg-variables)

[func NewReader(r io.Reader) (io.ReadCloser, error)](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#NewReader)

[func NewReaderDict(r io.Reader, dict [\]byte) (io.ReadCloser, error)](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#NewReaderDict)

[type Writer](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#Writer)

- [func NewWriter(w io.Writer) *Writer](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#NewWriter)
- [func NewWriterLevel(w io.Writer, level int) (*Writer, error)](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#NewWriterLevel)
- [func NewWriterLevelDict(w io.Writer, level int, dict [\]byte) (*Writer, error)](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#NewWriterLevelDict)
- [func (z *Writer) Close() error](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#Writer.Close)
- [func (z *Writer) Flush() error](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#Writer.Flush)
- [func (z *Writer) Reset(w io.Writer)](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#Writer.Reset)
- [func (z *Writer) Write(p [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#Writer.Write)

#### Examples

返回首页



[NewReader](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#example-NewReader)

[NewWriter](https://studygolang.com/static/pkgdoc/pkg/compress_zlib.htm#example-NewWriter)

### Constants

```go
const (
    NoCompression      = flate.NoCompression
    BestSpeed          = flate.BestSpeed
    BestCompression    = flate.BestCompression
    DefaultCompression = flate.DefaultCompression
)
```

这些常量都是拷贝自flate包，因此导入"compress/zlib"后，就不必再导入"compress/flate"了。

### Variables

```go
var (
    // 当读取的zlib数据的校验和错误时，会返回ErrChecksum
    ErrChecksum = errors.New("zlib: invalid checksum")
    // 当读取的zlib数据的目录错误时，会返回ErrDictionary
    ErrDictionary = errors.New("zlib: invalid dictionary")
    // 当读取的zlib数据的头域错误时，会返回ErrHeader
    ErrHeader = errors.New("zlib: invalid header")
)
```

### func [NewReader](https://github.com/golang/go/blob/master/src/compress/zlib/reader.go?name=release#58)

```go
func NewReader(r io.Reader) (io.ReadCloser, error)
```

NewReader返回一个从r读取并解压数据的io.ReadCloser。其实现会缓冲输入流的数据，并可能从r中读取比需要的更多的数据。调用者有责任在读取完毕后调用返回值的Close方法。

Example

```go
buff := []byte{120, 156, 202, 72, 205, 201, 201, 215, 81, 40, 207,
    47, 202, 73, 225, 2, 4, 0, 0, 255, 255, 33, 231, 4, 147}
b := bytes.NewReader(buff)
r, err := zlib.NewReader(b)
if err != nil {
    panic(err)
}
io.Copy(os.Stdout, r)
```

Output:

```go
hello, world
```

### func [NewReaderDict](https://github.com/golang/go/blob/master/src/compress/zlib/reader.go?name=release#64)

```go
func NewReaderDict(r io.Reader, dict []byte) (io.ReadCloser, error)
```

NewReaderDict类似NewReader，但会使用预设的字典初始化返回的Reader。

如果压缩数据没有采用字典，本函数会忽略该参数。

### type [Writer](https://github.com/golang/go/blob/master/src/compress/zlib/writer.go?name=release#26)

```go
type Writer struct {
    // 内含隐藏或非导出字段
}
```

Writer将提供给它的数据压缩后写入下层io.Writer接口。

#### func [NewWriter](https://github.com/golang/go/blob/master/src/compress/zlib/writer.go?name=release#42)

```go
func NewWriter(w io.Writer) *Writer
```

NewWriter创建并返回一个Writer。写入返回值的数据都会在压缩后写入w。

调用者有责任在结束写入后调用返回值的Close方法。因为写入的数据可能保存在缓冲中没有刷新入下层。

Example

```go
var b bytes.Buffer
w := zlib.NewWriter(&b)
w.Write([]byte("hello, world\n"))
w.Close()
fmt.Println(b.Bytes())
```

Output:

```go
[120 156 202 72 205 201 201 215 81 40 207 47 202 73 225 2 4 0 0 255 255 33 231 4 147]
```

#### func [NewWriterLevel](https://github.com/golang/go/blob/master/src/compress/zlib/writer.go?name=release#53)

```go
func NewWriterLevel(w io.Writer, level int) (*Writer, error)
```

NewWriterLevel类似NewWriter但指定了压缩水平而不是采用默认的DefaultCompression。

参数level可以是DefaultCompression、NoCompression或BestSpeed与BestCompression之间包括二者的任何整数。如果level合法，返回的错误值为nil。

#### func [NewWriterLevelDict](https://github.com/golang/go/blob/master/src/compress/zlib/writer.go?name=release#62)

```go
func NewWriterLevelDict(w io.Writer, level int, dict []byte) (*Writer, error)
```

NewWriterLevelDict类似NewWriterLevel但还指定了用于压缩的字典。dict参数可以为nil；否则，在返回的Writer关闭之前，其内容不可被修改。

#### func (*Writer) [Reset](https://github.com/golang/go/blob/master/src/compress/zlib/writer.go?name=release#76)

```go
func (z *Writer) Reset(w io.Writer)
```

Reset将w重置，丢弃当前的写入状态，并将下层输出目标设为dst。效果上等价于将w设为使用dst和w的压缩水平、字典重新调用NewWriterLevel或NewWriterLevelDict返回的*Writer。

#### func (*Writer) [Write](https://github.com/golang/go/blob/master/src/compress/zlib/writer.go?name=release#146)

```go
func (z *Writer) Write(p []byte) (n int, err error)
```

Write将p压缩后写入下层io.Writer接口。压缩后的数据不一定会立刻刷新，除非Writer被关闭或者显式的刷新。

#### func (*Writer) [Flush](https://github.com/golang/go/blob/master/src/compress/zlib/writer.go?name=release#166)

```go
func (z *Writer) Flush() error
```

Flush将缓冲中的压缩数据刷新到下层io.Writer接口中。

#### func (*Writer) [Close](https://github.com/golang/go/blob/master/src/compress/zlib/writer.go?name=release#179)

```go
func (z *Writer) Close() error
```

调用Close会刷新缓冲并关闭w，但不会关闭下层io.Writer接口。

# container/heap

## package heap

```go
import "container/heap"
```

heap包提供了对任意类型（实现了heap.Interface接口）的堆操作。（最小）堆是具有“每个节点都是以其为根的子树中最小值”属性的树。

树的最小元素为其根元素，索引0的位置。

heap是常用的实现优先队列的方法。要创建一个优先队列，实现一个具有使用（负的）优先级作为比较的依据的Less方法的Heap接口，如此一来可用Push添加项目而用Pop取出队列最高优先级的项目。

Example (IntHeap)

```go
// This example demonstrates an integer heap built using the heap interface.
package heap_test
import (
    "container/heap"
    "fmt"
)
// An IntHeap is a min-heap of ints.
type IntHeap []int
func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *IntHeap) Push(x interface{}) {
    // Push and Pop use pointer receivers because they modify the slice's length,
    // not just its contents.
    *h = append(*h, x.(int))
}
func (h *IntHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[0 : n-1]
    return x
}
// This example inserts several ints into an IntHeap, checks the minimum,
// and removes them in order of priority.
func Example_intHeap() {
    h := &IntHeap{2, 1, 5}
    heap.Init(h)
    heap.Push(h, 3)
    fmt.Printf("minimum: %d\n", (*h)[0])
    for h.Len() > 0 {
        fmt.Printf("%d ", heap.Pop(h))
    }
    // Output:
    // minimum: 1
    // 1 2 3 5
}
```

Example (PriorityQueue)

```go
// This example demonstrates a priority queue built using the heap interface.
package heap_test
import (
    "container/heap"
    "fmt"
)
// An Item is something we manage in a priority queue.
type Item struct {
    value    string // The value of the item; arbitrary.
    priority int    // The priority of the item in the queue.
    // The index is needed by update and is maintained by the heap.Interface methods.
    index int // The index of the item in the heap.
}
// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item
func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool {
    // We want Pop to give us the highest, not lowest, priority so we use greater than here.
    return pq[i].priority > pq[j].priority
}
func (pq PriorityQueue) Swap(i, j int) {
    pq[i], pq[j] = pq[j], pq[i]
    pq[i].index = i
    pq[j].index = j
}
func (pq *PriorityQueue) Push(x interface{}) {
    n := len(*pq)
    item := x.(*Item)
    item.index = n
    *pq = append(*pq, item)
}
func (pq *PriorityQueue) Pop() interface{} {
    old := *pq
    n := len(old)
    item := old[n-1]
    item.index = -1 // for safety
    *pq = old[0 : n-1]
    return item
}
// update modifies the priority and value of an Item in the queue.
func (pq *PriorityQueue) update(item *Item, value string, priority int) {
    item.value = value
    item.priority = priority
    heap.Fix(pq, item.index)
}
// This example creates a PriorityQueue with some items, adds and manipulates an item,
// and then removes the items in priority order.
func Example_priorityQueue() {
    // Some items and their priorities.
    items := map[string]int{
        "banana": 3, "apple": 2, "pear": 4,
    }
    // Create a priority queue, put the items in it, and
    // establish the priority queue (heap) invariants.
    pq := make(PriorityQueue, len(items))
    i := 0
    for value, priority := range items {
        pq[i] = &Item{
            value:    value,
            priority: priority,
            index:    i,
        }
        i++
    }
    heap.Init(&pq)
    // Insert a new item and then modify its priority.
    item := &Item{
        value:    "orange",
        priority: 1,
    }
    heap.Push(&pq, item)
    pq.update(item, item.value, 5)
    // Take the items out; they arrive in decreasing priority order.
    for pq.Len() > 0 {
        item := heap.Pop(&pq).(*Item)
        fmt.Printf("%.2d:%s ", item.priority, item.value)
    }
    // Output:
    // 05:orange 04:pear 03:banana 02:apple
}
```

### Index

返回首页



[type Interface](https://studygolang.com/static/pkgdoc/pkg/container_heap.htm#Interface)

[func Init(h Interface)](https://studygolang.com/static/pkgdoc/pkg/container_heap.htm#Init)

[func Push(h Interface, x interface{})](https://studygolang.com/static/pkgdoc/pkg/container_heap.htm#Push)

[func Pop(h Interface) interface{}](https://studygolang.com/static/pkgdoc/pkg/container_heap.htm#Pop)

[func Remove(h Interface, i int) interface{}](https://studygolang.com/static/pkgdoc/pkg/container_heap.htm#Remove)

[func Fix(h Interface, i int)](https://studygolang.com/static/pkgdoc/pkg/container_heap.htm#Fix)

#### Examples

返回首页



[package (IntHeap)](https://studygolang.com/static/pkgdoc/pkg/container_heap.htm#example-package--IntHeap)

[package (PriorityQueue)](https://studygolang.com/static/pkgdoc/pkg/container_heap.htm#example-package--PriorityQueue)

### type [Interface](https://github.com/golang/go/blob/master/src/container/heap/heap.go?name=release#30)

```go
type Interface interface {
    sort.Interface
    Push(x interface{}) // 向末尾添加元素
    Pop() interface{}   // 从末尾删除元素
}
```

任何实现了本接口的类型都可以用于构建最小堆。最小堆可以通过heap.Init建立，数据是递增顺序或者空的话也是最小堆。最小堆的约束条件是：

```go
!h.Less(j, i) for 0 <= i < h.Len() and 2*i+1 <= j <= 2*i+2 and j < h.Len()
```

注意接口的Push和Pop方法是供heap包调用的，请使用heap.Push和heap.Pop来向一个堆添加或者删除元素。

### func [Init](https://github.com/golang/go/blob/master/src/container/heap/heap.go?name=release#41)

```go
func Init(h Interface)
```

一个堆在使用任何堆操作之前应先初始化。Init函数对于堆的约束性是幂等的（多次执行无意义），并可能在任何时候堆的约束性被破坏时被调用。本函数复杂度为O(n)，其中n等于h.Len()。

### func [Push](https://github.com/golang/go/blob/master/src/container/heap/heap.go?name=release#52)

```go
func Push(h Interface, x interface{})
```

向堆h中插入元素x，并保持堆的约束性。复杂度O(log(n))，其中n等于h.Len()。

### func [Pop](https://github.com/golang/go/blob/master/src/container/heap/heap.go?name=release#61)

```go
func Pop(h Interface) interface{}
```

删除并返回堆h中的最小元素（不影响约束性）。复杂度O(log(n))，其中n等于h.Len()。等价于Remove(h, 0)。

### func [Remove](https://github.com/golang/go/blob/master/src/container/heap/heap.go?name=release#71)

```go
func Remove(h Interface, i int) interface{}
```

删除堆中的第i个元素，并保持堆的约束性。复杂度O(log(n))，其中n等于h.Len()。

### func [Fix](https://github.com/golang/go/blob/master/src/container/heap/heap.go?name=release#85)

```go
func Fix(h Interface, i int)
```

在修改第i个元素后，调用本函数修复堆，比删除第i个元素后插入新元素更有效率。

复杂度O(log(n))，其中n等于h.Len()。

# container/list

## package list

```go
import "container/list"
```

list包实现了双向链表。要遍历一个链表：

```go
for e := l.Front(); e != nil; e = e.Next() {
	// do something with e.Value
}
```

Example

```go
// Create a new list and put some numbers in it.
l := list.New()
e4 := l.PushBack(4)
e1 := l.PushFront(1)
l.InsertBefore(3, e4)
l.InsertAfter(2, e1)
// Iterate through list and print its contents.
for e := l.Front(); e != nil; e = e.Next() {
    fmt.Println(e.Value)
}
```

Output:

```go
1
2
3
4
```

### Index

返回首页



[type Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#Element)

- [func (e *Element) Next() *Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#Element.Next)
- [func (e *Element) Prev() *Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#Element.Prev)

[type List](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List)

- [func New() *List](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#New)
- [func (l *List) Init() *List](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.Init)
- [func (l *List) Len() int](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.Len)
- [func (l *List) Front() *Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.Front)
- [func (l *List) Back() *Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.Back)
- [func (l *List) PushFront(v interface{}) *Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.PushFront)
- [func (l *List) PushFrontList(other *List)](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.PushFrontList)
- [func (l *List) PushBack(v interface{}) *Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.PushBack)
- [func (l *List) PushBackList(other *List)](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.PushBackList)
- [func (l *List) InsertBefore(v interface{}, mark *Element) *Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.InsertBefore)
- [func (l *List) InsertAfter(v interface{}, mark *Element) *Element](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.InsertAfter)
- [func (l *List) MoveToFront(e *Element)](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.MoveToFront)
- [func (l *List) MoveToBack(e *Element)](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.MoveToBack)
- [func (l *List) MoveBefore(e, mark *Element)](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.MoveBefore)
- [func (l *List) MoveAfter(e, mark *Element)](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.MoveAfter)
- [func (l *List) Remove(e *Element) interface{}](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#List.Remove)

#### Examples

返回首页



[package](https://studygolang.com/static/pkgdoc/pkg/container_list.htm#example-package)

### type [Element](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#15)

```go
type Element struct {
    // 元素保管的值
    Value interface{}
    // 内含隐藏或非导出字段
}
```

Element类型代表是双向链表的一个元素。

#### func (*Element) [Next](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#31)

```go
func (e *Element) Next() *Element
```

Next返回链表的后一个元素或者nil。

#### func (*Element) [Prev](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#39)

```go
func (e *Element) Prev() *Element
```

Prev返回链表的前一个元素或者nil。

### type [List](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#48)

```go
type List struct {
    // 内含隐藏或非导出字段
}
```

List代表一个双向链表。List零值为一个空的、可用的链表。

#### func [New](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#62)

```go
func New() *List
```

New创建一个链表。

#### func (*List) [Init](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#54)

```go
func (l *List) Init() *List
```

Init清空链表。

#### func (*List) [Len](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#66)

```go
func (l *List) Len() int
```

Len返回链表中元素的个数，复杂度O(1)。

#### func (*List) [Front](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#69)

```go
func (l *List) Front() *Element
```

Front返回链表第一个元素或nil。

#### func (*List) [Back](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#77)

```go
func (l *List) Back() *Element
```

Back返回链表最后一个元素或nil。

#### func (*List) [PushFront](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#131)

```go
func (l *List) PushFront(v interface{}) *Element
```

PushBack将一个值为v的新元素插入链表的第一个位置，返回生成的新元素。

#### func (*List) [PushFrontList](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#211)

```go
func (l *List) PushFrontList(other *List)
```

PushFrontList创建链表other的拷贝，并将拷贝的最后一个位置连接到链表l的第一个位置。

#### func (*List) [PushBack](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#137)

```go
func (l *List) PushBack(v interface{}) *Element
```

PushBack将一个值为v的新元素插入链表的最后一个位置，返回生成的新元素。

#### func (*List) [PushBackList](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#202)

```go
func (l *List) PushBackList(other *List)
```

PushBack创建链表other的拷贝，并将链表l的最后一个位置连接到拷贝的第一个位置。

#### func (*List) [InsertBefore](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#144)

```go
func (l *List) InsertBefore(v interface{}, mark *Element) *Element
```

InsertBefore将一个值为v的新元素插入到mark前面，并返回生成的新元素。如果mark不是l的元素，l不会被修改。

#### func (*List) [InsertAfter](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#154)

```go
func (l *List) InsertAfter(v interface{}, mark *Element) *Element
```

InsertAfter将一个值为v的新元素插入到mark后面，并返回新生成的元素。如果mark不是l的元素，l不会被修改。

#### func (*List) [MoveToFront](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#164)

```go
func (l *List) MoveToFront(e *Element)
```

MoveToFront将元素e移动到链表的第一个位置，如果e不是l的元素，l不会被修改。

#### func (*List) [MoveToBack](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#174)

```go
func (l *List) MoveToBack(e *Element)
```

MoveToBack将元素e移动到链表的最后一个位置，如果e不是l的元素，l不会被修改。

#### func (*List) [MoveBefore](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#184)

```go
func (l *List) MoveBefore(e, mark *Element)
```

MoveBefore将元素e移动到mark的前面。如果e或mark不是l的元素，或者e==mark，l不会被修改。

#### func (*List) [MoveAfter](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#193)

```go
func (l *List) MoveAfter(e, mark *Element)
```

MoveAfter将元素e移动到mark的后面。如果e或mark不是l的元素，或者e==mark，l不会被修改。

#### func (*List) [Remove](https://github.com/golang/go/blob/master/src/container/list/list.go?name=release#121)

```go
func (l *List) Remove(e *Element) interface{}
```

Remove删除链表中的元素e，并返回e.Value。

# container/ring

## package ring

```go
import "container/ring"
```

ring实现了环形链表的操作。

### Index

返回首页



[type Ring](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#Ring)

- [func New(n int) *Ring](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#New)
- [func (r *Ring) Len() int](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#Ring.Len)
- [func (r *Ring) Next() *Ring](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#Ring.Next)
- [func (r *Ring) Prev() *Ring](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#Ring.Prev)
- [func (r *Ring) Move(n int) *Ring](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#Ring.Move)
- [func (r *Ring) Link(s *Ring) *Ring](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#Ring.Link)
- [func (r *Ring) Unlink(n int) *Ring](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#Ring.Unlink)
- [func (r *Ring) Do(f func(interface{}))](https://studygolang.com/static/pkgdoc/pkg/container_ring.htm#Ring.Do)





### type [Ring](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#14)

```go
type Ring struct {
    Value interface{} // 供调用者使用，本包不会操作该字段
    // 包含隐藏或非导出字段
}
```

Ring类型代表环形链表的一个元素，同时也代表链表本身。环形链表没有头尾；指向环形链表任一元素的指针都可以作为整个环形链表看待。Ring零值是具有一个（Value字段为nil的）元素的链表。

#### func [New](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#62)

```go
func New(n int) *Ring
```

New创建一个具有n个元素的环形链表。

#### func (*Ring) [Len](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#121)

```go
func (r *Ring) Len() int
```

Len返回环形链表中的元素个数，复杂度O(n)。

#### func (*Ring) [Next](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#26)

```go
func (r *Ring) Next() *Ring
```

返回后一个元素，r不能为空。

#### func (*Ring) [Prev](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#34)

```go
func (r *Ring) Prev() *Ring
```

返回前一个元素，r不能为空。

#### func (*Ring) [Move](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#44)

```go
func (r *Ring) Move(n int) *Ring
```

返回移动n个位置（n>=0向前移动，n<0向后移动）后的元素，r不能为空。

#### func (*Ring) [Link](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#93)

```go
func (r *Ring) Link(s *Ring) *Ring
```

Link连接r和s，并返回r原本的后继元素r.Next()。r不能为空。

如果r和s指向同一个环形链表，则会删除掉r和s之间的元素，删掉的元素构成一个子链表，返回指向该子链表的指针（r的原后继元素）；如果没有删除元素，则仍然返回r的原后继元素，而不是nil。如果r和s指向不同的链表，将创建一个单独的链表，将s指向的链表插入r后面，返回s原最后一个元素后面的元素（即r的原后继元素）。

#### func (*Ring) [Unlink](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#111)

```go
func (r *Ring) Unlink(n int) *Ring
```

删除链表中n % r.Len()个元素，从r.Next()开始删除。如果n % r.Len() == 0，不修改r。返回删除的元素构成的链表，r不能为空。

#### func (*Ring) [Do](https://github.com/golang/go/blob/master/src/container/ring/ring.go?name=release#134)

```go
func (r *Ring) Do(f func(interface{}))
```

对链表的每一个元素都执行f（正向顺序），注意如果f改变了*r，Do的行为是未定义的。

# context

## package context

```go
import "context"
```

Package context defines the Context type, which carries deadlines, cancelation signals, and other request-scoped values across API boundaries and between processes.

Incoming requests to a server should create a Context, and outgoing calls to servers should accept a Context. The chain of function calls between them must propagate the Context, optionally replacing it with a derived Context created using WithCancel, WithDeadline, WithTimeout, or WithValue. When a Context is canceled, all Contexts derived from it are also canceled.

The WithCancel, WithDeadline, and WithTimeout functions take a Context (the parent) and return a derived Context (the child) and a CancelFunc. Calling the CancelFunc cancels the child and its children, removes the parent's reference to the child, and stops any associated timers. Failing to call the CancelFunc leaks the child and its children until the parent is canceled or the timer fires. The go vet tool checks that CancelFuncs are used on all control-flow paths.

Programs that use Contexts should follow these rules to keep interfaces consistent across packages and enable static analysis tools to check context propagation:

Do not store Contexts inside a struct type; instead, pass a Context explicitly to each function that needs it. The Context should be the first parameter, typically named ctx:

```go
func DoSomething(ctx context.Context, arg Arg) error {
	// ... use ctx ...
}
```

Do not pass a nil Context, even if a function permits it. Pass context.TODO if you are unsure about which Context to use.

Use context Values only for request-scoped data that transits processes and APIs, not for passing optional parameters to functions.

The same Context may be passed to functions running in different goroutines; Contexts are safe for simultaneous use by multiple goroutines.

See <https://blog.golang.org/context> for example code for a server that uses Contexts.

### Index

返回首页



- [Variables](https://studygolang.com/static/pkgdoc/pkg/context.htm#pkg-variables)

- [type CancelFunc](https://studygolang.com/static/pkgdoc/pkg/context.htm#CancelFunc)

- [type Context](https://studygolang.com/static/pkgdoc/pkg/context.htm#Context)

- - [func Background() Context](https://studygolang.com/static/pkgdoc/pkg/context.htm#Background)
  - [func TODO() Context](https://studygolang.com/static/pkgdoc/pkg/context.htm#TODO)
  - [func WithCancel(parent Context) (ctx Context, cancel CancelFunc)](https://studygolang.com/static/pkgdoc/pkg/context.htm#WithCancel)
  - [func WithDeadline(parent Context, deadline time.Time) (Context, CancelFunc)](https://studygolang.com/static/pkgdoc/pkg/context.htm#WithDeadline)
  - [func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)](https://studygolang.com/static/pkgdoc/pkg/context.htm#WithTimeout)
  - [func WithValue(parent Context, key, val interface{}) Context](https://studygolang.com/static/pkgdoc/pkg/context.htm#WithValue)

#### Examples

- [WithCancel](https://studygolang.com/static/pkgdoc/pkg/context.htm#example-WithCancel)
- [WithDeadline](https://studygolang.com/static/pkgdoc/pkg/context.htm#example-WithDeadline)
- [WithTimeout](https://studygolang.com/static/pkgdoc/pkg/context.htm#example-WithTimeout)
- [WithValue](https://studygolang.com/static/pkgdoc/pkg/context.htm#example-WithValue)

#### [Package Files](https://github.com/golang/go/blob/master/src/context/)

[context.go](https://github.com/golang/go/blob/master/src/context/context.go)

### Variables

❖

```go
var Canceled = errors.New("context canceled")
```

Canceled is the error returned by Context.Err when the context is canceled.

❖

```go
var DeadlineExceeded error = deadlineExceededError{}
```

DeadlineExceeded is the error returned by Context.Err when the context's deadline passes.

### type [CancelFunc](https://github.com/golang/go/blob/master/src/context/context.go#L221)

❖

```go
type CancelFunc func()
```

A CancelFunc tells an operation to abandon its work. A CancelFunc does not wait for the work to stop. After the first call, subsequent calls to a CancelFunc do nothing.

### type [Context](https://github.com/golang/go/blob/master/src/context/context.go#L62)

❖

```go
type Context interface {
    // Deadline returns the time when work done on behalf of this context
    // should be canceled. Deadline returns ok==false when no deadline is
    // set. Successive calls to Deadline return the same results.
    Deadline() (deadline time.Time, ok bool)

    // Done returns a channel that's closed when work done on behalf of this
    // context should be canceled. Done may return nil if this context can
    // never be canceled. Successive calls to Done return the same value.
    //
    // WithCancel arranges for Done to be closed when cancel is called;
    // WithDeadline arranges for Done to be closed when the deadline
    // expires; WithTimeout arranges for Done to be closed when the timeout
    // elapses.
    //
    // Done is provided for use in select statements:
    //
    //  // Stream generates values with DoSomething and sends them to out
    //  // until DoSomething returns an error or ctx.Done is closed.
    //  func Stream(ctx context.Context, out chan<- Value) error {
    //  	for {
    //  		v, err := DoSomething(ctx)
    //  		if err != nil {
    //  			return err
    //  		}
    //  		select {
    //  		case <-ctx.Done():
    //  			return ctx.Err()
    //  		case out <- v:
    //  		}
    //  	}
    //  }
    //
    // See https://blog.golang.org/pipelines for more examples of how to use
    // a Done channel for cancelation.
    Done() <-chan struct{}

    // Err returns a non-nil error value after Done is closed. Err returns
    // Canceled if the context was canceled or DeadlineExceeded if the
    // context's deadline passed. No other values for Err are defined.
    // After Done is closed, successive calls to Err return the same value.
    Err() error

    // Value returns the value associated with this context for key, or nil
    // if no value is associated with key. Successive calls to Value with
    // the same key returns the same result.
    //
    // Use context values only for request-scoped data that transits
    // processes and API boundaries, not for passing optional parameters to
    // functions.
    //
    // A key identifies a specific value in a Context. Functions that wish
    // to store values in Context typically allocate a key in a global
    // variable then use that key as the argument to context.WithValue and
    // Context.Value. A key can be any type that supports equality;
    // packages should define keys as an unexported type to avoid
    // collisions.
    //
    // Packages that define a Context key should provide type-safe accessors
    // for the values stored using that key:
    //
    // 	// Package user defines a User type that's stored in Contexts.
    // 	package user
    //
    // 	import "context"
    //
    // 	// User is the type of value stored in the Contexts.
    // 	type User struct {...}
    //
    // 	// key is an unexported type for keys defined in this package.
    // 	// This prevents collisions with keys defined in other packages.
    // 	type key int
    //
    // 	// userKey is the key for user.User values in Contexts. It is
    // 	// unexported; clients use user.NewContext and user.FromContext
    // 	// instead of using this key directly.
    // 	var userKey key = 0
    //
    // 	// NewContext returns a new Context that carries value u.
    // 	func NewContext(ctx context.Context, u *User) context.Context {
    // 		return context.WithValue(ctx, userKey, u)
    // 	}
    //
    // 	// FromContext returns the User value stored in ctx, if any.
    // 	func FromContext(ctx context.Context) (*User, bool) {
    // 		u, ok := ctx.Value(userKey).(*User)
    // 		return u, ok
    // 	}
    Value(key interface{}) interface{}
}
```

A Context carries a deadline, a cancelation signal, and other values across API boundaries.

Context's methods may be called by multiple goroutines simultaneously.

#### func [Background](https://github.com/golang/go/blob/master/src/context/context.go#L205)

❖

```go
func Background() Context
```

Background returns a non-nil, empty Context. It is never canceled, has no values, and has no deadline. It is typically used by the main function, initialization, and tests, and as the top-level Context for incoming requests.

#### func [TODO](https://github.com/golang/go/blob/master/src/context/context.go#L214)

❖

```go
func TODO() Context
```

TODO returns a non-nil, empty Context. Code should use context.TODO when it's unclear which Context to use or it is not yet available (because the surrounding function has not yet been extended to accept a Context parameter). TODO is recognized by static analysis tools that determine whether Contexts are propagated correctly in a program.

#### func [WithCancel](https://github.com/golang/go/blob/master/src/context/context.go#L229)

❖

```go
func WithCancel(parent Context) (ctx Context, cancel CancelFunc)
```

WithCancel returns a copy of parent with a new Done channel. The returned context's Done channel is closed when the returned cancel function is called or when the parent context's Done channel is closed, whichever happens first.

Canceling this context releases resources associated with it, so code should call cancel as soon as the operations running in this Context complete.

[Example](https://studygolang.com/static/pkgdoc/pkg/context.htm#ex-WithCancel)



This example demonstrates the use of a cancelable context to prevent a goroutine leak. By the end of the example function, the goroutine started by gen will return without leaking.

Code:[play](https://studygolang.com/static/pkgdoc/pkg/context.htm?play=WithCancel) 

```
// gen generates integers in a separate goroutine and
// sends them to the returned channel.
// The callers of gen need to cancel the context once
// they are done consuming generated integers not to leak
// the internal goroutine started by gen.
gen := func(ctx context.Context) <-chan int {
    dst := make(chan int)
    n := 1
    go func() {
        for {
            select {
            case <-ctx.Done():
                return // returning not to leak the goroutine
            case dst <- n:
                n++
            }
        }
    }()
    return dst
}

ctx, cancel := context.WithCancel(context.Background())
defer cancel() // cancel when we are finished consuming integers

for n := range gen(ctx) {
    fmt.Println(n)
    if n == 5 {
        break
    }
}
```

Output:

```
1
2
3
4
5
```

#### func [WithDeadline](https://github.com/golang/go/blob/master/src/context/context.go#L369)

❖

```
func WithDeadline(parent Context, deadline time.Time) (Context, CancelFunc)
```

WithDeadline returns a copy of the parent context with the deadline adjusted to be no later than d. If the parent's deadline is already earlier than d, WithDeadline(parent, d) is semantically equivalent to parent. The returned context's Done channel is closed when the deadline expires, when the returned cancel function is called, or when the parent context's Done channel is closed, whichever happens first.

Canceling this context releases resources associated with it, so code should call cancel as soon as the operations running in this Context complete.

[Example](https://studygolang.com/static/pkgdoc/pkg/context.htm#ex-WithDeadline)



This example passes a context with a arbitrary deadline to tell a blocking function that it should abandon its work as soon as it gets to it.

Code:[play](https://studygolang.com/static/pkgdoc/pkg/context.htm?play=WithDeadline) 

```go
d := time.Now().Add(50 * time.Millisecond)
ctx, cancel := context.WithDeadline(context.Background(), d)

// Even though ctx will be expired, it is good practice to call its
// cancelation function in any case. Failure to do so may keep the
// context and its parent alive longer than necessary.
defer cancel()

select {
case <-time.After(1 * time.Second):
    fmt.Println("overslept")
case <-ctx.Done():
    fmt.Println(ctx.Err())
}
```

Output:

```go
context deadline exceeded
```

#### func [WithTimeout](https://github.com/golang/go/blob/master/src/context/context.go#L436)

❖

```go
func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)
```

WithTimeout returns WithDeadline(parent, time.Now().Add(timeout)).

Canceling this context releases resources associated with it, so code should call cancel as soon as the operations running in this Context complete:

```go
func slowOperationWithTimeout(ctx context.Context) (Result, error) {
	ctx, cancel := context.WithTimeout(ctx, 100*time.Millisecond)
	defer cancel()  // releases resources if slowOperation completes before timeout elapses
	return slowOperation(ctx)
}
```

[Example](https://studygolang.com/static/pkgdoc/pkg/context.htm#ex-WithTimeout)



This example passes a context with a timeout to tell a blocking function that it should abandon its work after the timeout elapses.

Code:[play](https://studygolang.com/static/pkgdoc/pkg/context.htm?play=WithTimeout) 

```
// Pass a context with a timeout to tell a blocking function that it
// should abandon its work after the timeout elapses.
ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
defer cancel()

select {
case <-time.After(1 * time.Second):
    fmt.Println("overslept")
case <-ctx.Done():
    fmt.Println(ctx.Err()) // prints "context deadline exceeded"
}
```

Output:

```
context deadline exceeded
```

#### func [WithValue](https://github.com/golang/go/blob/master/src/context/context.go#L453)

❖

```
func WithValue(parent Context, key, val interface{}) Context
```

WithValue returns a copy of parent in which the value associated with key is val.

Use context Values only for request-scoped data that transits processes and APIs, not for passing optional parameters to functions.

The provided key must be comparable and should not be of type string or any other built-in type to avoid collisions between packages using context. Users of WithValue should define their own types for keys. To avoid allocating when assigning to an interface{}, context keys often have concrete type struct{}. Alternatively, exported context key variables' static type should be a pointer or interface.

[Example](https://studygolang.com/static/pkgdoc/pkg/context.htm#ex-WithValue)

Code:

```go
type favContextKey string

f := func(ctx context.Context, k favContextKey) {
    if v := ctx.Value(k); v != nil {
        fmt.Println("found value:", v)
        return
    }
    fmt.Println("key not found:", k)
}

k := favContextKey("language")
ctx := context.WithValue(context.Background(), k, "Go")

f(ctx, k)
f(ctx, favContextKey("color"))
```

Output:

```go
found value: Go
key not found: color
```

# crypto

## package crypto

```go
import "crypto"
```

crypto包搜集了常用的密码（算法）常量。

### Index

返回首页



[type PublicKey](https://studygolang.com/static/pkgdoc/pkg/crypto.htm#PublicKey)

[type PrivateKey](https://studygolang.com/static/pkgdoc/pkg/crypto.htm#PrivateKey)

[type Hash](https://studygolang.com/static/pkgdoc/pkg/crypto.htm#Hash)

- [func (h Hash) Available() bool](https://studygolang.com/static/pkgdoc/pkg/crypto.htm#Hash.Available)
- [func (h Hash) Size() int](https://studygolang.com/static/pkgdoc/pkg/crypto.htm#Hash.Size)
- [func (h Hash) New() hash.Hash](https://studygolang.com/static/pkgdoc/pkg/crypto.htm#Hash.New)

[func RegisterHash(h Hash, f func() hash.Hash)](https://studygolang.com/static/pkgdoc/pkg/crypto.htm#RegisterHash)

### type [PublicKey](https://github.com/golang/go/blob/master/src/crypto/crypto.go?name=release#82)

```go
type PublicKey interface{}
```

代表一个使用未指定算法的公钥。

### type [PrivateKey](https://github.com/golang/go/blob/master/src/crypto/crypto.go?name=release#85)

```go
type PrivateKey interface{}
```

代表一个使用未指定算法的私钥。

### type [Hash](https://github.com/golang/go/blob/master/src/crypto/crypto.go?name=release#15)

```go
type Hash uint
```

Hash用来识别/标识另一个包里实现的加密函数。

```go
const (
    MD4       Hash = 1 + iota // 导入code.google.com/p/go.crypto/md4
    MD5                       // 导入crypto/md5
    SHA1                      // 导入crypto/sha1
    SHA224                    // 导入crypto/sha256
    SHA256                    // 导入crypto/sha256
    SHA384                    // 导入crypto/sha512
    SHA512                    // 导入crypto/sha512
    MD5SHA1                   // 未实现；MD5+SHA1用于TLS RSA
    RIPEMD160                 // 导入code.google.com/p/go.crypto/ripemd160
)
```

#### func (Hash) [Available](https://github.com/golang/go/blob/master/src/crypto/crypto.go?name=release#67)

```go
func (h Hash) Available() bool
```

报告是否有hash函数注册到该标识值。

#### func (Hash) [Size](https://github.com/golang/go/blob/master/src/crypto/crypto.go?name=release#45)

```go
func (h Hash) Size() int
```

返回给定hash函数返回值的字节长度。

#### func (Hash) [New](https://github.com/golang/go/blob/master/src/crypto/crypto.go?name=release#56)

```go
func (h Hash) New() hash.Hash
```

创建一个使用给定hash函数的hash.Hash接口，如果该标识值未注册hash函数，将会panic。

### func [RegisterHash](https://github.com/golang/go/blob/master/src/crypto/crypto.go?name=release#74)

```go
func RegisterHash(h Hash, f func() hash.Hash)
```

注册一个返回给定hash接口实例的函数，并指定其标识值，该函数应在实现hash接口的包的init函数中调用。

# crypto/aes

## package aes

```go
import "crypto/aes"
```

aes包实现了AES加密算法，参见U.S. Federal Information Processing Standards Publication 197。

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/crypto_aes.htm#pkg-constants)

[type KeySizeError](https://studygolang.com/static/pkgdoc/pkg/crypto_aes.htm#KeySizeError)

- [func (k KeySizeError) Error() string](https://studygolang.com/static/pkgdoc/pkg/crypto_aes.htm#KeySizeError.Error)

[func NewCipher(key [\]byte) (cipher.Block, error)](https://studygolang.com/static/pkgdoc/pkg/crypto_aes.htm#NewCipher)

### Constants

```go
const BlockSize = 16
```

AES字节块大小。

### type [KeySizeError](https://github.com/golang/go/blob/master/src/crypto/aes/cipher.go?name=release#21)

```go
type KeySizeError int
```

#### func (KeySizeError) [Error](https://github.com/golang/go/blob/master/src/crypto/aes/cipher.go?name=release#23)

```go
func (k KeySizeError) Error() string
```

### func [NewCipher](https://github.com/golang/go/blob/master/src/crypto/aes/cipher.go?name=release#31)

```go
func NewCipher(key []byte) (cipher.Block, error)
```

创建一个cipher.Block接口。参数key为密钥，长度只能是16、24、32字节，用以选择AES-128、AES-192、AES-256。

# crypto/cipher

## package cipher

```go
import "crypto/cipher"
```

cipher包实现了多个标准的用于包装底层块加密算法的加密算法实现。

参见<http://csrc.nist.gov/groups/ST/toolkit/BCM/current_modes.html>和NIST Special Publication 800-38A。

### Index

返回首页



[type Block](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#Block)

[type BlockMode](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#BlockMode)

- [func NewCBCDecrypter(b Block, iv [\]byte) BlockMode](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#NewCBCDecrypter)
- [func NewCBCEncrypter(b Block, iv [\]byte) BlockMode](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#NewCBCEncrypter)

[type Stream](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#Stream)

- [func NewCFBDecrypter(block Block, iv [\]byte) Stream](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#NewCFBDecrypter)
- [func NewCFBEncrypter(block Block, iv [\]byte) Stream](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#NewCFBEncrypter)
- [func NewCTR(block Block, iv [\]byte) Stream](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#NewCTR)
- [func NewOFB(b Block, iv [\]byte) Stream](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#NewOFB)

[type StreamReader](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#StreamReader)

- [func (r StreamReader) Read(dst [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#StreamReader.Read)

[type StreamWriter](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#StreamWriter)

- [func (w StreamWriter) Write(src [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#StreamWriter.Write)
- [func (w StreamWriter) Close() error](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#StreamWriter.Close)

[type AEAD](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#AEAD)

- [func NewGCM(cipher Block) (AEAD, error)](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#NewGCM)

#### Examples

返回首页



[NewCBCDecrypter](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#example-NewCBCDecrypter)

[NewCBCEncrypter](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#example-NewCBCEncrypter)

[NewCFBDecrypter](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#example-NewCFBDecrypter)

[NewCFBEncrypter](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#example-NewCFBEncrypter)

[NewCTR](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#example-NewCTR)

[NewOFB](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#example-NewOFB)

[StreamReader](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#example-StreamReader)

[StreamWriter](https://studygolang.com/static/pkgdoc/pkg/crypto_cipher.htm#example-StreamWriter)

### type [Block](https://github.com/golang/go/blob/master/src/crypto/cipher/cipher.go?name=release#15)

```go
type Block interface {
    // 返回加密字节块的大小
    BlockSize() int
    // 加密src的第一块数据并写入dst，src和dst可指向同一内存地址
    Encrypt(dst, src []byte)
    // 解密src的第一块数据并写入dst，src和dst可指向同一内存地址
    Decrypt(dst, src []byte)
}
```

Block接口代表一个使用特定密钥的底层块加/解密器。它提供了加密和解密独立数据块的能力。

### type [BlockMode](https://github.com/golang/go/blob/master/src/crypto/cipher/cipher.go?name=release#37)

```go
type BlockMode interface {
    // 返回加密字节块的大小
    BlockSize() int
    // 加密或解密连续的数据块，src的尺寸必须是块大小的整数倍，src和dst可指向同一内存地址
    CryptBlocks(dst, src []byte)
}
```

BlockMode接口代表一个工作在块模式（如CBC、ECB等）的加/解密器。

#### func [NewCBCEncrypter](https://github.com/golang/go/blob/master/src/crypto/cipher/cbc.go?name=release#35)

```go
func NewCBCEncrypter(b Block, iv []byte) BlockMode
```

返回一个密码分组链接模式的、底层用b加密的BlockMode接口，初始向量iv的长度必须等于b的块尺寸。

Example

```go
key := []byte("example key 1234")
plaintext := []byte("exampleplaintext")
// CBC mode works on blocks so plaintexts may need to be padded to the
// next whole block. For an example of such padding, see
// https://tools.ietf.org/html/rfc5246#section-6.2.3.2. Here we'll
// assume that the plaintext is already of the correct length.
if len(plaintext)%aes.BlockSize != 0 {
    panic("plaintext is not a multiple of the block size")
}
block, err := aes.NewCipher(key)
if err != nil {
    panic(err)
}
// The IV needs to be unique, but not secure. Therefore it's common to
// include it at the beginning of the ciphertext.
ciphertext := make([]byte, aes.BlockSize+len(plaintext))
iv := ciphertext[:aes.BlockSize]
if _, err := io.ReadFull(rand.Reader, iv); err != nil {
    panic(err)
}
mode := cipher.NewCBCEncrypter(block, iv)
mode.CryptBlocks(ciphertext[aes.BlockSize:], plaintext)
// It's important to remember that ciphertexts must be authenticated
// (i.e. by using crypto/hmac) as well as being encrypted in order to
// be secure.
fmt.Printf("%x\n", ciphertext)
```

#### func [NewCBCDecrypter](https://github.com/golang/go/blob/master/src/crypto/cipher/cbc.go?name=release#81)

```go
func NewCBCDecrypter(b Block, iv []byte) BlockMode
```

返回一个密码分组链接模式的、底层用b解密的BlockMode接口，初始向量iv必须和加密时使用的iv相同。

Example

```go
key := []byte("example key 1234")
ciphertext, _ := hex.DecodeString("f363f3ccdcb12bb883abf484ba77d9cd7d32b5baecb3d4b1b3e0e4beffdb3ded")
block, err := aes.NewCipher(key)
if err != nil {
    panic(err)
}
// The IV needs to be unique, but not secure. Therefore it's common to
// include it at the beginning of the ciphertext.
if len(ciphertext) < aes.BlockSize {
    panic("ciphertext too short")
}
iv := ciphertext[:aes.BlockSize]
ciphertext = ciphertext[aes.BlockSize:]
// CBC mode always works in whole blocks.
if len(ciphertext)%aes.BlockSize != 0 {
    panic("ciphertext is not a multiple of the block size")
}
mode := cipher.NewCBCDecrypter(block, iv)
// CryptBlocks can work in-place if the two arguments are the same.
mode.CryptBlocks(ciphertext, ciphertext)
// If the original plaintext lengths are not a multiple of the block
// size, padding would have to be added when encrypting, which would be
// removed at this point. For an example, see
// https://tools.ietf.org/html/rfc5246#section-6.2.3.2. However, it's
// critical to note that ciphertexts must be authenticated (i.e. by
// using crypto/hmac) before being decrypted in order to avoid creating
// a padding oracle.
fmt.Printf("%s\n", ciphertext)
```

Output:

```go
exampleplaintext
```

### type [Stream](https://github.com/golang/go/blob/master/src/crypto/cipher/cipher.go?name=release#29)

```go
type Stream interface {
    // 从加密器的key流和src中依次取出字节二者xor后写入dst，src和dst可指向同一内存地址
    XORKeyStream(dst, src []byte)
}
```

Stream接口代表一个流模式的加/解密器。

#### func [NewCFBEncrypter](https://github.com/golang/go/blob/master/src/crypto/cipher/cfb.go?name=release#45)

```go
func NewCFBEncrypter(block Block, iv []byte) Stream
```

返回一个密码反馈模式的、底层用block加密的Stream接口，初始向量iv的长度必须等于block的块尺寸。

Example

```go
key := []byte("example key 1234")
plaintext := []byte("some plaintext")
block, err := aes.NewCipher(key)
if err != nil {
    panic(err)
}
// The IV needs to be unique, but not secure. Therefore it's common to
// include it at the beginning of the ciphertext.
ciphertext := make([]byte, aes.BlockSize+len(plaintext))
iv := ciphertext[:aes.BlockSize]
if _, err := io.ReadFull(rand.Reader, iv); err != nil {
    panic(err)
}
stream := cipher.NewCFBEncrypter(block, iv)
stream.XORKeyStream(ciphertext[aes.BlockSize:], plaintext)
// It's important to remember that ciphertexts must be authenticated
// (i.e. by using crypto/hmac) as well as being encrypted in order to
// be secure.
```

#### func [NewCFBDecrypter](https://github.com/golang/go/blob/master/src/crypto/cipher/cfb.go?name=release#52)

```go
func NewCFBDecrypter(block Block, iv []byte) Stream
```

返回一个密码反馈模式的、底层用block解密的Stream接口，初始向量iv必须和加密时使用的iv相同。

Example

```go
key := []byte("example key 1234")
ciphertext, _ := hex.DecodeString("22277966616d9bc47177bd02603d08c9a67d5380d0fe8cf3b44438dff7b9")
block, err := aes.NewCipher(key)
if err != nil {
    panic(err)
}
// The IV needs to be unique, but not secure. Therefore it's common to
// include it at the beginning of the ciphertext.
if len(ciphertext) < aes.BlockSize {
    panic("ciphertext too short")
}
iv := ciphertext[:aes.BlockSize]
ciphertext = ciphertext[aes.BlockSize:]
stream := cipher.NewCFBDecrypter(block, iv)
// XORKeyStream can work in-place if the two arguments are the same.
stream.XORKeyStream(ciphertext, ciphertext)
fmt.Printf("%s", ciphertext)
```

Output:

```go
some plaintext
```

#### func [NewOFB](https://github.com/golang/go/blob/master/src/crypto/cipher/ofb.go?name=release#19)

```go
func NewOFB(b Block, iv []byte) Stream
```

返回一个输出反馈模式的、底层采用b生成key流的Stream接口，初始向量iv的长度必须等于b的块尺寸。

Example

```go
key := []byte("example key 1234")
plaintext := []byte("some plaintext")
block, err := aes.NewCipher(key)
if err != nil {
    panic(err)
}
// The IV needs to be unique, but not secure. Therefore it's common to
// include it at the beginning of the ciphertext.
ciphertext := make([]byte, aes.BlockSize+len(plaintext))
iv := ciphertext[:aes.BlockSize]
if _, err := io.ReadFull(rand.Reader, iv); err != nil {
    panic(err)
}
stream := cipher.NewOFB(block, iv)
stream.XORKeyStream(ciphertext[aes.BlockSize:], plaintext)
// It's important to remember that ciphertexts must be authenticated
// (i.e. by using crypto/hmac) as well as being encrypted in order to
// be secure.
// OFB mode is the same for both encryption and decryption, so we can
// also decrypt that ciphertext with NewOFB.
plaintext2 := make([]byte, len(plaintext))
stream = cipher.NewOFB(block, iv)
stream.XORKeyStream(plaintext2, ciphertext[aes.BlockSize:])
fmt.Printf("%s\n", plaintext2)
```

Output:

```go
some plaintext
```

#### func [NewCTR](https://github.com/golang/go/blob/master/src/crypto/cipher/ctr.go?name=release#26)

```go
func NewCTR(block Block, iv []byte) Stream
```

返回一个计数器模式的、底层采用block生成key流的Stream接口，初始向量iv的长度必须等于block的块尺寸。

Example

```go
key := []byte("example key 1234")
plaintext := []byte("some plaintext")
block, err := aes.NewCipher(key)
if err != nil {
    panic(err)
}
// The IV needs to be unique, but not secure. Therefore it's common to
// include it at the beginning of the ciphertext.
ciphertext := make([]byte, aes.BlockSize+len(plaintext))
iv := ciphertext[:aes.BlockSize]
if _, err := io.ReadFull(rand.Reader, iv); err != nil {
    panic(err)
}
stream := cipher.NewCTR(block, iv)
stream.XORKeyStream(ciphertext[aes.BlockSize:], plaintext)
// It's important to remember that ciphertexts must be authenticated
// (i.e. by using crypto/hmac) as well as being encrypted in order to
// be secure.
// CTR mode is the same for both encryption and decryption, so we can
// also decrypt that ciphertext with NewCTR.
plaintext2 := make([]byte, len(plaintext))
stream = cipher.NewCTR(block, iv)
stream.XORKeyStream(plaintext2, ciphertext[aes.BlockSize:])
fmt.Printf("%s\n", plaintext2)
```

Output:

```go
some plaintext
```

### type [StreamReader](https://github.com/golang/go/blob/master/src/crypto/cipher/io.go?name=release#14)

```go
type StreamReader struct {
    S   Stream
    R   io.Reader
}
```

将一个Stream与一个io.Reader接口关联起来，Read方法会调用XORKeyStream方法来处理获取的所有切片。

Example

```go
key := []byte("example key 1234")
inFile, err := os.Open("encrypted-file")
if err != nil {
    panic(err)
}
defer inFile.Close()
block, err := aes.NewCipher(key)
if err != nil {
    panic(err)
}
// If the key is unique for each ciphertext, then it's ok to use a zero
// IV.
var iv [aes.BlockSize]byte
stream := cipher.NewOFB(block, iv[:])
outFile, err := os.OpenFile("decrypted-file", os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0600)
if err != nil {
    panic(err)
}
defer outFile.Close()
reader := &cipher.StreamReader{S: stream, R: inFile}
// Copy the input file to the output file, decrypting as we go.
if _, err := io.Copy(outFile, reader); err != nil {
    panic(err)
}
// Note that this example is simplistic in that it omits any
// authentication of the encrypted data. It you were actually to use
// StreamReader in this manner, an attacker could flip arbitrary bits in
// the output.
```

#### func (StreamReader) [Read](https://github.com/golang/go/blob/master/src/crypto/cipher/io.go?name=release#19)

```go
func (r StreamReader) Read(dst []byte) (n int, err error)
```

### type [StreamWriter](https://github.com/golang/go/blob/master/src/crypto/cipher/io.go?name=release#30)

```go
type StreamWriter struct {
    S   Stream
    W   io.Writer
    Err error // unused
}
```

将一个Stream与一个io.Writer接口关联起来，Write方法会调用XORKeyStream方法来处理提供的所有切片。如果Write方法返回的n小于提供的切片的长度，则表示StreamWriter不同步，必须丢弃。StreamWriter没有内建的缓存，不需要调用Close方法去清空缓存。

Example

```go
key := []byte("example key 1234")
inFile, err := os.Open("plaintext-file")
if err != nil {
    panic(err)
}
defer inFile.Close()
block, err := aes.NewCipher(key)
if err != nil {
    panic(err)
}
// If the key is unique for each ciphertext, then it's ok to use a zero
// IV.
var iv [aes.BlockSize]byte
stream := cipher.NewOFB(block, iv[:])
outFile, err := os.OpenFile("encrypted-file", os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0600)
if err != nil {
    panic(err)
}
defer outFile.Close()
writer := &cipher.StreamWriter{S: stream, W: outFile}
// Copy the input file to the output file, encrypting as we go.
if _, err := io.Copy(writer, inFile); err != nil {
    panic(err)
}
// Note that this example is simplistic in that it omits any
// authentication of the encrypted data. It you were actually to use
// StreamReader in this manner, an attacker could flip arbitrary bits in
// the decrypted result.
```

#### func (StreamWriter) [Write](https://github.com/golang/go/blob/master/src/crypto/cipher/io.go?name=release#36)

```go
func (w StreamWriter) Write(src []byte) (n int, err error)
```

#### func (StreamWriter) [Close](https://github.com/golang/go/blob/master/src/crypto/cipher/io.go?name=release#50)

```go
func (w StreamWriter) Close() error
```

如果w.W字段实现了io.Closer接口，本方法会调用其Close方法并返回该方法的返回值；否则不做操作返回nil。

### type [AEAD](https://github.com/golang/go/blob/master/src/crypto/cipher/gcm.go?name=release#14)

```go
type AEAD interface {
    // 返回提供给Seal和Open方法的随机数nonce的字节长度
    NonceSize() int
    // 返回原始文本和加密文本的最大长度差异
    Overhead() int
    // 加密并认证明文，认证附加的data，将结果添加到dst，返回更新后的切片。
    // nonce的长度必须是NonceSize()字节，且对给定的key和时间都是独一无二的。
    // plaintext和dst可以是同一个切片，也可以不同。
    Seal(dst, nonce, plaintext, data []byte) []byte
    // 解密密文并认证，认证附加的data，如果认证成功，将明文添加到dst，返回更新后的切片。
    // nonce的长度必须是NonceSize()字节，nonce和data都必须和加密时使用的相同。
    // ciphertext和dst可以是同一个切片，也可以不同。
    Open(dst, nonce, ciphertext, data []byte) ([]byte, error)
}
```

AEAD接口是一种提供了使用关联数据进行认证加密的功能的加密模式。

#### func [NewGCM](https://github.com/golang/go/blob/master/src/crypto/cipher/gcm.go?name=release#62)

```go
func NewGCM(cipher Block) (AEAD, error)
```

函数用迦洛瓦计数器模式包装提供的128位Block接口，并返回AEAD接口。

# crypto/des

## package des

```go
import "crypto/des"
```

des包实现了DES标准和TDEA算法，参见U.S. Federal Information Processing Standards Publication 46-3。

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/crypto_des.htm#pkg-constants)

[type KeySizeError](https://studygolang.com/static/pkgdoc/pkg/crypto_des.htm#KeySizeError)

- [func (k KeySizeError) Error() string](https://studygolang.com/static/pkgdoc/pkg/crypto_des.htm#KeySizeError.Error)

[func NewCipher(key [\]byte) (cipher.Block, error)](https://studygolang.com/static/pkgdoc/pkg/crypto_des.htm#NewCipher)

[func NewTripleDESCipher(key [\]byte) (cipher.Block, error)](https://studygolang.com/static/pkgdoc/pkg/crypto_des.htm#NewTripleDESCipher)

### Constants

```go
const BlockSize = 8
```

DES字节块的大小。

### type [KeySizeError](https://github.com/golang/go/blob/master/src/crypto/des/cipher.go?name=release#15)

```go
type KeySizeError int
```

#### func (KeySizeError) [Error](https://github.com/golang/go/blob/master/src/crypto/des/cipher.go?name=release#17)

```go
func (k KeySizeError) Error() string
```

### func [NewCipher](https://github.com/golang/go/blob/master/src/crypto/des/cipher.go?name=release#27)

```go
func NewCipher(key []byte) (cipher.Block, error)
```

创建并返回一个使用DES算法的cipher.Block接口。

### func [NewTripleDESCipher](https://github.com/golang/go/blob/master/src/crypto/des/cipher.go?name=release#49)

```go
func NewTripleDESCipher(key []byte) (cipher.Block, error)
```

创建并返回一个使用TDEA算法的cipher.Block接口。

Example

```go
// NewTripleDESCipher can also be used when EDE2 is required by
// duplicating the first 8 bytes of the 16-byte key.
ede2Key := []byte("example key 1234")
var tripleDESKey []byte
tripleDESKey = append(tripleDESKey, ede2Key[:16]...)
tripleDESKey = append(tripleDESKey, ede2Key[:8]...)
_, err := des.NewTripleDESCipher(tripleDESKey)
if err != nil {
    panic(err)
}
// See crypto/cipher for how to use a cipher.Block for encryption and
// decryption.
```

# crypto/dsa

## package dsa

```go
import "crypto/dsa"
```

dsa包实现FIPS 186-3定义的数字签名算法（Digital Signature Algorithm），即DSA算法。

### Index

返回首页



[Variables](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#pkg-variables)

[type ParameterSizes](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#ParameterSizes)

[type Parameters](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#Parameters)

[type PublicKey](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#PublicKey)

[type PrivateKey](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#PrivateKey)

[func GenerateParameters(params *Parameters, rand io.Reader, sizes ParameterSizes) (err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#GenerateParameters)

[func GenerateKey(priv *PrivateKey, rand io.Reader) error](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#GenerateKey)

[func Sign(rand io.Reader, priv *PrivateKey, hash [\]byte) (r, s *big.Int, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#Sign)

[func Verify(pub *PublicKey, hash [\]byte, r, s *big.Int) bool](https://studygolang.com/static/pkgdoc/pkg/crypto_dsa.htm#Verify)

### Variables

```go
var ErrInvalidPublicKey = errors.New("crypto/dsa: invalid public key")
```

非法公钥，FIPS标准的公钥格式是很严格的，但有些实现没这么严格，使用这些实现的公钥时，就会导致这个错误。

### type [ParameterSizes](https://github.com/golang/go/blob/master/src/crypto/dsa/dsa.go?name=release#40)

```go
type ParameterSizes int
```

是DSA参数中的质数可以接受的字位长度的枚举，参见FIPS 186-3 section 4.2。

```go
const (
    L1024N160 ParameterSizes = iota
    L2048N224
    L2048N256
    L3072N256
)
```

### type [Parameters](https://github.com/golang/go/blob/master/src/crypto/dsa/dsa.go?name=release#16)

```go
type Parameters struct {
    P, Q, G *big.Int
}
```

Parameters代表密钥的域参数，这些参数可以被一组密钥共享，Q的字位长度必须是8的倍数。

### type [PublicKey](https://github.com/golang/go/blob/master/src/crypto/dsa/dsa.go?name=release#21)

```go
type PublicKey struct {
    Parameters
    Y   *big.Int
}
```

PublicKey代表一个DSA公钥。

### type [PrivateKey](https://github.com/golang/go/blob/master/src/crypto/dsa/dsa.go?name=release#27)

```go
type PrivateKey struct {
    PublicKey
    X   *big.Int
}
```

PrivateKey代表一个DSA私钥。

### func [GenerateKey](https://github.com/golang/go/blob/master/src/crypto/dsa/dsa.go?name=release#151)

### func [GenerateParameters](https://github.com/golang/go/blob/master/src/crypto/dsa/dsa.go?name=release#55)

```go
func GenerateParameters(params *Parameters, rand io.Reader, sizes ParameterSizes) (err error)
```

GenerateParameters函数随机设置合法的参数到params。即使机器很快，函数也可能会花费很多时间来生成参数。

```go
func GenerateKey(priv *PrivateKey, rand io.Reader) error
```

GenerateKey生成一对公钥和私钥；priv.PublicKey.Parameters字段必须已经（被GenerateParameters函数）设置了合法的参数。

### func [Sign](https://github.com/golang/go/blob/master/src/crypto/dsa/dsa.go?name=release#194)

```go
func Sign(rand io.Reader, priv *PrivateKey, hash []byte) (r, s *big.Int, err error)
```

使用私钥对任意长度的hash值（必须是较大信息的hash结果）进行签名，返回签名结果（一对大整数）。私钥的安全性取决于密码读取器的熵度（随机程度）。

注意根据FIPS 186-3 section 4.6的规定，hash必须被截断到亚组的长度，本函数是不会自己截断的。

### func [Verify](https://github.com/golang/go/blob/master/src/crypto/dsa/dsa.go?name=release#249)

```go
func Verify(pub *PublicKey, hash []byte, r, s *big.Int) bool
```

使用公钥认证hash和两个大整数r、s构成的签名，报告签名是否合法。

注意根据FIPS 186-3 section 4.6的规定，hash必须被截断到亚组的长度，本函数是不会自己截断的。

# crypto/ecdsa

## package ecdsa

```go
import "crypto/ecdsa"
```

ecdsa包实现了椭圆曲线数字签名算法，参见FIPS 186-3。

### Index

返回首页



[type PublicKey](https://studygolang.com/static/pkgdoc/pkg/crypto_ecdsa.htm#PublicKey)

[type PrivateKey](https://studygolang.com/static/pkgdoc/pkg/crypto_ecdsa.htm#PrivateKey)

- [func GenerateKey(c elliptic.Curve, rand io.Reader) (priv *PrivateKey, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_ecdsa.htm#GenerateKey)

[func Sign(rand io.Reader, priv *PrivateKey, hash [\]byte) (r, s *big.Int, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_ecdsa.htm#Sign)

[func Verify(pub *PublicKey, hash [\]byte, r, s *big.Int) bool](https://studygolang.com/static/pkgdoc/pkg/crypto_ecdsa.htm#Verify)

### type [PublicKey](https://github.com/golang/go/blob/master/src/crypto/ecdsa/ecdsa.go?name=release#22)

```go
type PublicKey struct {
    elliptic.Curve
    X, Y *big.Int
}
```

PrivateKey代表一个ECDSA公钥。

### type [PrivateKey](https://github.com/golang/go/blob/master/src/crypto/ecdsa/ecdsa.go?name=release#28)

```go
type PrivateKey struct {
    PublicKey
    D   *big.Int
}
```

PrivateKey代表一个ECDSA私钥。

#### func [GenerateKey](https://github.com/golang/go/blob/master/src/crypto/ecdsa/ecdsa.go?name=release#53)

GenerateKey函数生成一对

```go
func GenerateKey(c elliptic.Curve, rand io.Reader) (priv *PrivateKey, err error)
```

公钥/私钥。

### func [Sign](https://github.com/golang/go/blob/master/src/crypto/ecdsa/ecdsa.go?name=release#101)

```go
func Sign(rand io.Reader, priv *PrivateKey, hash []byte) (r, s *big.Int, err error)
```

使用私钥对任意长度的hash值（必须是较大信息的hash结果）进行签名，返回签名结果（一对大整数）。私钥的安全性取决于密码读取器的熵度（随机程度）。

### func [Verify](https://github.com/golang/go/blob/master/src/crypto/ecdsa/ecdsa.go?name=release#138)

```go
func Verify(pub *PublicKey, hash []byte, r, s *big.Int) bool
```

使用公钥验证hash值和两个大整数r、s构成的签名，并返回签名是否合法。

# crypto/elliptic

## package elliptic

```go
import "crypto/elliptic"
```

elliptic包实现了几条覆盖素数有限域的标准椭圆曲线。

### Index

返回首页



[type Curve](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#Curve)

- [func P224() Curve](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#P224)
- [func P256() Curve](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#P256)
- [func P384() Curve](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#P384)
- [func P521() Curve](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#P521)

[type CurveParams](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#CurveParams)

- [func (curve *CurveParams) Add(x1, y1, x2, y2 *big.Int) (*big.Int, *big.Int)](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#CurveParams.Add)
- [func (curve *CurveParams) Double(x1, y1 *big.Int) (*big.Int, *big.Int)](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#CurveParams.Double)
- [func (curve *CurveParams) IsOnCurve(x, y *big.Int) bool](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#CurveParams.IsOnCurve)
- [func (curve *CurveParams) Params() *CurveParams](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#CurveParams.Params)
- [func (curve *CurveParams) ScalarBaseMult(k [\]byte) (*big.Int, *big.Int)](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#CurveParams.ScalarBaseMult)
- [func (curve *CurveParams) ScalarMult(Bx, By *big.Int, k [\]byte) (*big.Int, *big.Int)](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#CurveParams.ScalarMult)

[func GenerateKey(curve Curve, rand io.Reader) (priv [\]byte, x, y *big.Int, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#GenerateKey)

[func Marshal(curve Curve, x, y *big.Int) [\]byte](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#Marshal)

[func Unmarshal(curve Curve, data [\]byte) (x, y *big.Int)](https://studygolang.com/static/pkgdoc/pkg/crypto_elliptic.htm#Unmarshal)

### type [Curve](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#24)

```go
type Curve interface {
    // Params返回椭圆曲线的参数
    Params() *CurveParams
    // IsOnCurve判断一个点是否在椭圆曲线上
    IsOnCurve(x, y *big.Int) bool
    // 返回点(x1,y1)和点(x2,y2)相加的结果
    Add(x1, y1, x2, y2 *big.Int) (x, y *big.Int)
    // 返回2*(x,y)，即(x,y)+(x,y)
    Double(x1, y1 *big.Int) (x, y *big.Int)
    // k是一个大端在前格式的数字，返回k*(Bx,By)
    ScalarMult(x1, y1 *big.Int, k []byte) (x, y *big.Int)
    // k是一个大端在前格式的数字，返回k*G，G是本椭圆曲线的基点
    ScalarBaseMult(k []byte) (x, y *big.Int)
}
```

Curve代表一个短格式的Weierstrass椭圆曲线，其中a=-3。

Weierstrass椭圆曲线的格式：y**2 = x**3 + a*x + b

参见<http://www.hyperelliptic.org/EFD/g1p/auto-shortw.html>

#### func [P224](https://github.com/golang/go/blob/master/src/crypto/elliptic/p224.go?name=release#39)

```go
func P224() Curve
```

返回一个实现了P-224的曲线。（参见FIPS 186-3, section D.2.2）

#### func [P256](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#358)

```go
func P256() Curve
```

返回一个实现了P-256的曲线。（参见FIPS 186-3, section D.2.3）

#### func [P384](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#364)

```go
func P384() Curve
```

返回一个实现了P-384的曲线。（参见FIPS 186-3, section D.2.4）

#### func [P521](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#370)

```go
func P521() Curve
```

返回一个实现了P-512的曲线。（参见FIPS 186-3, section D.2.5）

### type [CurveParams](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#42)

```go
type CurveParams struct {
    P       *big.Int // 决定有限域的p的值（必须是素数）
    N       *big.Int // 基点的阶（必须是素数）
    B       *big.Int // 曲线公式的常量（B!=2）
    Gx, Gy  *big.Int // 基点的坐标
    BitSize int      // 决定有限域的p的字位数
}
```

CurveParams包含一个椭圆曲线的所有参数，也可提供一般的、非常数时间实现的椭圆曲线。

#### func (*CurveParams) [Params](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#50)

```go
func (curve *CurveParams) Params() *CurveParams
```

#### func (*CurveParams) [IsOnCurve](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#54)

```go
func (curve *CurveParams) IsOnCurve(x, y *big.Int) bool
```

#### func (*CurveParams) [Add](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#101)

```go
func (curve *CurveParams) Add(x1, y1, x2, y2 *big.Int) (*big.Int, *big.Int)
```

#### func (*CurveParams) [Double](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#185)

```go
func (curve *CurveParams) Double(x1, y1 *big.Int) (*big.Int, *big.Int)
```

#### func (*CurveParams) [ScalarMult](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#250)

```go
func (curve *CurveParams) ScalarMult(Bx, By *big.Int, k []byte) (*big.Int, *big.Int)
```

#### func (*CurveParams) [ScalarBaseMult](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#267)

```go
func (curve *CurveParams) ScalarBaseMult(k []byte) (*big.Int, *big.Int)
```

### func [GenerateKey](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#275)

```go
func GenerateKey(curve Curve, rand io.Reader) (priv []byte, x, y *big.Int, err error)
```

GenerateKey返回一个公钥/私钥对。priv是私钥，而(x,y)是公钥。密钥对是通过提供的随机数读取器来生成的，该io.Reader接口必须返回随机数据。

### func [Marshal](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#297)

```go
func Marshal(curve Curve, x, y *big.Int) []byte
```

Marshal将一个点编码为ANSI X9.62指定的格式。

### func [Unmarshal](https://github.com/golang/go/blob/master/src/crypto/elliptic/elliptic.go?name=release#311)

```go
func Unmarshal(curve Curve, data []byte) (x, y *big.Int)
```

将一个Marshal编码后的点还原；如果出错，x会被设为nil。

# crypto/hmac

## package hmac

```go
import "crypto/hmac"
```

hmac包实现了U.S. Federal Information Processing Standards Publication 198规定的HMAC（加密哈希信息认证码）。

HMAC是使用key标记信息的加密hash。接收者使用相同的key逆运算来认证hash。

出于安全目的，接收者应使用Equal函数比较认证码：

```go
// 如果messageMAC是message的合法HMAC标签，函数返回真
func CheckMAC(message, messageMAC, key []byte) bool {
	mac := hmac.New(sha256.New, key)
	mac.Write(message)
	expectedMAC := mac.Sum(nil)
	return hmac.Equal(messageMAC, expectedMAC)
}
```

### Index

返回首页



[func Equal(mac1, mac2 [\]byte) bool](https://studygolang.com/static/pkgdoc/pkg/crypto_hmac.htm#Equal)

[func New(h func() hash.Hash, key [\]byte) hash.Hash](https://studygolang.com/static/pkgdoc/pkg/crypto_hmac.htm#New)

### func [Equal](https://github.com/golang/go/blob/master/src/crypto/hmac/hmac.go?name=release#97)

```go
func Equal(mac1, mac2 []byte) bool
```

比较两个MAC是否相同，而不会泄露对比时间信息。（以规避时间侧信道攻击：指通过计算比较时花费的时间的长短来获取密码的信息，用于密码破解）

### func [New](https://github.com/golang/go/blob/master/src/crypto/hmac/hmac.go?name=release#78)

```go
func New(h func() hash.Hash, key []byte) hash.Hash
```

New函数返回一个采用hash.Hash作为底层hash接口、key作为密钥的HMAC算法的hash接口。

# crypto/md5

## package md5

```go
import "crypto/md5"
```

md5包实现了MD5哈希算法，参见[RFC 1321](http://tools.ietf.org/html/rfc1321)。

### Index

返回首页



[Constants](https://studygolang.com/static/pkgdoc/pkg/crypto_md5.htm#pkg-constants)

[func Sum(data [\]byte) [Size]byte](https://studygolang.com/static/pkgdoc/pkg/crypto_md5.htm#Sum)

[func New() hash.Hash](https://studygolang.com/static/pkgdoc/pkg/crypto_md5.htm#New)

#### Examples

返回首页



[New](https://studygolang.com/static/pkgdoc/pkg/crypto_md5.htm#example-New)

[Sum](https://studygolang.com/static/pkgdoc/pkg/crypto_md5.htm#example-Sum)

### Constants

```go
const BlockSize = 64
```

MD5字节块大小。

```go
const Size = 16
```

MD5校验和字节数。

### func [Sum](https://github.com/golang/go/blob/master/src/crypto/md5/md5.go?name=release#129)

```go
func Sum(data []byte) [Size]byte
```

返回数据data的MD5校验和。

Example

```go
data := []byte("These pretzels are making me thirsty.")
fmt.Printf("%x", md5.Sum(data))
```

Output:

```go
b0804ec967f48520697662a204f5fe72
```

### func [New](https://github.com/golang/go/blob/master/src/crypto/md5/md5.go?name=release#49)

```go
func New() hash.Hash
```

返回一个新的使用MD5校验的hash.Hash接口。

Example

```go
h := md5.New()
io.WriteString(h, "The fog is getting thicker!")
io.WriteString(h, "And Leon's getting laaarger!")
fmt.Printf("%x", h.Sum(nil))
```

Output:

```go
e2c569be17396eca2a2e3c11578123ed
```

# crypto/rand

## package rand

```go
import "crypto/rand"
```

rand包实现了用于加解密的更安全的随机数生成器。

### Index

返回首页



[Variables](https://studygolang.com/static/pkgdoc/pkg/crypto_rand.htm#pkg-variables)

[func Int(rand io.Reader, max *big.Int) (n *big.Int, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_rand.htm#Int)

[func Prime(rand io.Reader, bits int) (p *big.Int, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_rand.htm#Prime)

[func Read(b [\]byte) (n int, err error)](https://studygolang.com/static/pkgdoc/pkg/crypto_rand.htm#Read)

#### Examples

返回首页



[Read](https://studygolang.com/static/pkgdoc/pkg/crypto_rand.htm#example-Read)

### Variables

```go
var Reader io.Reader
```

Reader是一个全局、共享的密码用强随机数生成器。在Unix类型系统中，会从/dev/urandom读取；而Windows中会调用CryptGenRandom API。

### func [Int](https://github.com/golang/go/blob/master/src/crypto/rand/util.go?name=release#106)

```go
func Int(rand io.Reader, max *big.Int) (n *big.Int, err error)
```

返回一个在[0, max)区间服从均匀分布的随机值，如果max<=0则会panic。

### func [Prime](https://github.com/golang/go/blob/master/src/crypto/rand/util.go?name=release#31)

```go
func Prime(rand io.Reader, bits int) (p *big.Int, err error)
```

返回一个具有指定字位数的数字，该数字具有很高可能性是质数。如果从rand读取时出错，或者bits<2会返回错误。

### func [Read](https://github.com/golang/go/blob/master/src/crypto/rand/rand.go?name=release#19)

```go
func Read(b []byte) (n int, err error)
```

本函数是一个使用io.ReadFull调用Reader.Read的辅助性函数。当且仅当err == nil时，返回值n == len(b)。

Example

```go
c := 10
b := make([]byte, c)
_, err := rand.Read(b)
if err != nil {
    fmt.Println("error:", err)
    return
}
// The slice should now contain random bytes instead of only zeroes.
fmt.Println(bytes.Equal(b, make([]byte, c)))
```

Output:

```go
false
```

