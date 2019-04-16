package storage
import (
    "gopkg.in/mgo.v2/bson"
    "time"
    "github.com/pmylund/go-cache"
    "strings"
    //"fmt"
)
const (
    defaultExpiration = 1*time.Minute      //缓存失效时间
    MatchExpiration = 15*time.Minute      //缓存失效时间
    purgesexpired = 15*time.Minute
)

var (
    c *cache.Cache =cache.New(defaultExpiration,purgesexpired)
)

func fetchCache(key string)(val interface{}, err error){
    val,found := c.Get(key)
    if !found{
        val,err = hgetAll(key)
        if err == nil && len(val.(map[string]string)) > 0 {
            c.Add(key,val,defaultExpiration)
        }
    }
    return val,err
}

func fetchCacheMatch(key string, fields []string)(val interface{}, err error){
    val,found := c.Get(key)
    if !found{
        val,err = hmget(key,fields)
        if err == nil && len(val.([]string)) > 0 {
            c.Add(key,val,MatchExpiration)
        }
    }
    return val,err
}

/**
黑名单缓存
 */
func SeachBlackList(collectionName,userId string) (result string,err error) {
    key := "BlackList"
    val,found := c.Get(key)
    if !found {
        fields := bson.M{"uid":userId}
        var temp []interface{}
        temp,err = SearchAll(collectionName,bson.M{"status":"1"},"uid",fields)
        //fmt.Println(temp)
        var user_arry []string
        for _,val := range temp {
            valMap := val.(bson.M)
            user_arry = append(user_arry,valMap["uid"].(string))
        }
        result = strings.Join(user_arry,",")
        if err == nil {
            c.Add(key,result,MatchExpiration)
        }
    }else{
        result = val.(string)
    }
    //fmt.Println(result)
    return
}

/**
缓存活动
 */
func FindOneActivity(collectionName,objectId string) (result interface{},err error) {
    key := "objectId:" + objectId
    val,found := c.Get(key)
    if !found {
        result,err = FindById(collectionName,objectId)
        if err == nil {
            query := bson.M{"activity_number": objectId}
            result_prize,err1 := SearchAll("prize_pool",query,"activity_number",nil)
            if err1 == nil {
                result.(bson.M)["prizes"] = result_prize
                c.Add(key,result,defaultExpiration)
            }
        }
    }else{
        result = val
    }
    return
}


