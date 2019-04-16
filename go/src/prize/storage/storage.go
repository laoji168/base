package storage

import "strings"

const (
    single_Client = 1
    more_Client = 300
)

func Storage_Init(redis_connect_str, redis_pass string, redis_db int, redis_usepipe, mongo_url, database string) {
    if strings.ToLower(redis_usepipe) == "ture" {
        RedisInit(redis_connect_str, redis_pass, redis_db, single_Client)
        proxy_init()
    } else {
        RedisInit(redis_connect_str, redis_pass, redis_db, more_Client)
    }
    mogoInit(mongo_url, database)
}

func HgetAll(key string) (map[string]string, error) {
    if strings.HasPrefix()
}