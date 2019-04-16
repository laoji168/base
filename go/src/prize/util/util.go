package util

import (
    "bytes"
    "crypto/md5"
    "encoding/binary"
    "encoding/hex"
    "fmt"
    "net/http"
    "os"
    "path/filepath"
    "strconv"
    "strings"
    "time"
)

//MD5 为字符串加盐
func MD5(str, key string) (res string) {
    m5 := md5.New()  //返回一个新的使用MD5校验的hash.Hash接口
    m5.Sum([]byte(str))  //返回数据data的MD5校验和
    m5.Write([]byte(key))  //为字符串加盐，返回字符数，err
    st := m5.Sum(nil)  //取得加盐后的校验和
    Infoln(st, hex.EncodeToString(st))  //输出日志信息校验和以及其十六进制表示
    res = hex.EncodeToString(st)
    return
}

//为字符串添加多个盐
func MD5_MUI(args ...string) (res string) {
    m5 := md5.New()
    for i, str := range args {
        if i == 0 {
            m5.Sum([]byte(str))
        }
        m5.Write([]byte(str))
    }
    st := m5.Sum(nil)
    Infoln(st, hex.EncodeToString(st))
    res = hex.EncodeToString(st)
    return
}

//字符串转md5十六进制字符串
func String2MD5(data string) string {
    input := []byte(data)
    sum := md5.Sum(input)
    res := ""
    for _, ch := range sum {
        res += fmt.Sprintf("%02x", ch)
    }
    return res
}

func UrlVerify(actId, t, key, matchId, clientMd5, userId string) bool {
    if userId == "null" || userId == "undefined" {
        return false
    }
    // step 1 验证tokeon&时效
    //当前时间戳
    timestamp := time.Now().Unix()
    temp, _ := strconv.ParseInt(t, 10, 64)
    time := timestamp - temp
    tokenServer := ""
    Debugln("time:", time)
    Debugln("timestamp:", timestamp)
    Debugln("temp:", temp)
    if time > 90000 {
        return false
    } else {
        tokenServer = String2MD5(actId+matchId+key)
        if tokenServer == clientMd5 {
            return true
        } else {
            return false
        }
    }
}

//整形转换成字节
func IntToBytes(n int) []byte {
    tmp := int32(n)
    bytesBuffer := bytes.NewBuffer([]byte{})
    //将tmp的binary编码格式写入bytesBuffer，
    //tmp必须是定长值、定长值的切片、定长值的指针。
    //binary.BigEndian指定写入数据的字节序，
    // 写入结构体时，名字中有'_'的字段会置为0。
    binary.Write(bytesBuffer, binary.BigEndian, tmp)
    return bytesBuffer.Bytes()
}

//字节转换成整形
func BytesToInt(b []byte) int {
    bytesBuffer := bytes.NewBuffer(b)
    var tmp int32
    binary.Read(bytesBuffer, binary.BigEndian, &tmp)
    return int(tmp)
}

func TimeParse(layout, value string) (time.Time, error) {
    loc, _ := time.LoadLocation("Local")  //获取时区信息
    //根据时区信息转换符合layout布局的value值
    _time, err := time.ParseInLocation(layout, value, loc)
    if err != nil {
        return time.Time{}, err
    }
    return _time, err
}

func StringInSlice(s string, slist []string) bool {
    for _, v := range slist {
        if s == v {
            return true
        }
    }
    return false
}

func SubString(s string, begin, end int) string {
    sbyte := []byte(s)
    if end > len(s) {
        end = len(s)
    }
    if begin > end {
        begin = end
    }
    if begin <= 0 {
        begin=0
    }
    return string(sbyte[begin:end])
}

func GetParentDirectory(directory string) string {
    return SubString(directory, 0, strings.LastIndex(directory, "/"))
}

func GetCurrentDirectory() string {
    dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
    if err != nil {
        Debugln(err)
    }
    return strings.Replace(dir, "\\", "/", -1)
}

func CookieString(c *http.Cookie) string {
    if c == nil {
        return ""
    }
    var b bytes.Buffer
    if len(c.Path) > 0 {
        b.WriteString(";Path=")
        b.WriteString(c.Path)
    }
    if len(c.Domain) > 0 {
        if c.Domain != "" {
            d := c.Domain
            b.WriteString("; Domain=")
            b.WriteString(d)
        } else {
            Infof("net/http:invalid Cookie.Domain %q; dropping domain attribute", c.Domain)
        }
    }
    if c.MaxAge > 0 {
        b.WriteString("; Max-Age=")
        b2 := b.Bytes()
        b.Reset()
        b.Write(strconv.AppendInt(b2, int64(c.MaxAge), 10))
    } else if c.MaxAge < 0 {
        b.WriteString("; Max-Age=0")
    }
    if c.HttpOnly {
        b.WriteString("; HttpOnly")
    }
    if c.Secure {
        b.WriteString("; Secure")
    }
    return b.String()
}