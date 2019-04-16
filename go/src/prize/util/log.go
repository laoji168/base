package util

import (
    "fmt"
    "log"
)

const (
    LevelDebug = (iota + 1) * 100
    LevelInfo
    LevelWarning
    LevelDatalog
    LevelError
)

var (
    levels = map[int]string {
        LevelDebug:     "DEBUG",
        LevelInfo:      "INFO",
        LevelWarning:   "WARNING",
        LevelDatalog:   "DATALOG",
        LevelError:     "ERROR",
    }
)

var loglevel int

//Setloglevel 设置日志等级
//参数：level string
//根据传入大写字符串，去映射levels中学习对应key
//为变量loglevel赋值为key
func Setloglevel(level string) {
    for k, v := range levels {
        if v == level {
            loglevel = k
        }
    }
}

//init 初始化
func init() {
    //设置标准logger的输出选项
    log.SetFlags(log.LstdFlags)
    //设置标准logger的输出前缀
    log.SetPrefix("[prize]\t")
}

func Debugln(v ...interface{}) {
    if LevelDebug < loglevel {
        return
    }
    s := fmt.Sprint(v ...)
    log.Println("DEBUG\t", s)
}

func Debugf(format string, v ...interface{}) {
    if LevelDebug < loglevel {
        return
    }
    format = "DEBUG\t" + format
    log.Printf(format, v...)
}

func Infoln(v ...interface{}) {
    if LevelInfo < loglevel {
        return
    }
    s := fmt.Sprint(v...)
    log.Println("INFO\t", s)
}

func Infof(format string, v ...interface{}) {
    if LevelInfo < loglevel {
        return
    }
    format = "INFO\t" + format
    log.Printf(format, v...)
}

func Warningln(v ...interface{}) {
    if LevelWarning < loglevel {
        return
    }
    s := fmt.Sprint(v...)
    log.Println("WARNING\t", s)
}

func Warningf(format string, v ...interface{}) {
    if LevelWarning < loglevel {
        return
    }
    format = "WARNING\t" + format
    log.Printf(format, v...)
}

func Errorln(v ...interface{}) {
    if LevelError < loglevel {
        return
    }
    s := fmt.Sprint(v...)
    log.Println("ERROR\t", s)
}

func Errorf(format string, v ...interface{}) {
    if LevelError < loglevel {
        return
    }
    format = "ERROR\t" + format
    log.Printf(format, v...)
}

func DataLogln(v ...interface{}) {
    s := fmt.Sprint(v...)
    log.Println("DATALOG/t", s)
}

func Datalogf(format string, v...interface{}) {
    format = "DATALOG/t" + format
    log.Printf(format, v...)
}

