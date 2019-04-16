package storage

import (
    "fmt"
    "github.com/garyburd/redigo/redis"
    "prize/util"
    "time"
)

var (
    pool *redis.Pool
    do func(cmd string, keys ...interface{}) (interface{}, error)
)

func RedisInit(redis_connect_str, redis_pass string, redis_db, client_num int) {
    pool = newPool(redis_connect_str, redis_pass, redis_db, client_num)
    if client_num == 1 {
        do = producer
    } else {
        do = redisDo
    }
}

func newPool(redis_connect_str, redis_pass string, redis_db, clients int) *redis.Pool {
    return &redis.Pool{
        MaxIdle:clients,
        Wait:true,
        IdleTimeout:240*time.Second,
        MaxActive:clients, //max number of connections
        Dial: func() (conn redis.Conn, e error) {
            db := redis.DialDatabase(redis_db)
            passwd := redis.DialPassword(redis_pass)
            connTimeout := redis.DialConnectTimeout(600*time.Second)
            readTimeout := redis.DialReadTimeout(60*time.Second)
            conn, e = redis.Dial("tcp", redis_connect_str, db, passwd, connTimeout, readTimeout)
            if e != nil {
                util.Errorln("redispool dial err:", e)
            }
            return conn, e
        },
        //Use the TestOnBorrow function to check the health
        //of an idle connection before the connection is returned
        //to the application
        TestOnBorrow: func(c redis.Conn, t time.Time) error {
            if time.Since(t) < time.Minute {
                return nil
            }
            _, err := c.Do("PING")
            return err
        },
    }
}

func redisDo(cmd string, keys ...interface{}) (v interface{}, err error) {
    defer func() {
        if e:=recover(); e!=nil {
            err = fmt.Errorf("redisDo %v", e)
        }
    }()
    c := pool.Get()
    defer c.Close()
    return c.Do(cmd, keys ...)
}