package my_test

import (
    "fmt"
    "net/http"
    "sort"
    "strconv"
    "strings"
)

const (
    pageTop    = `<!DOCTYPE HTML><html><head>
<style>.error{color:#FF0000;}</style></head><title>Statistics</title>
<body><h3>Statistics</h3>
<p>Computes basic statistics for a given list of numbers</p>`
    form       = `<form action="/" method="POST">
<label for="numbers">Numbers (comma or space-separated):</label><br />
<input type="text" name="numbers" size="30"><br />
<input type="submit" value="Calculate">
</form>`
    pageBottom = `</body></html>`
    anError    = `<p class="error">%s</p>`
)

type statistics struct {
    numbers []float64
    mean    float64
    median  float64
}

func processRequest(request *http.Request) ([]float64, string, bool) {
    var numbers [] float64
    // Form[key]的value形式为[]string,即单元素的字符串切片
    if slice, found := request.Form["numbers"]; found && len(slice) > 0 {
        text := strings.Replace(slice[0], ",", " ", -1)
        for _, field := range strings.Fields(text) {
            if x, err := strconv.ParseFloat(field, 64); err != nil {
                return numbers, "'" + field + "' is invalid", false 
            } else {
                numbers = append(numbers, x)
            }
        }
    }
    if len(numbers) == 0 {
        return numbers, "", false //第一次没有数据被显示
    }
    return numbers, "", true
}

func homePage(writer http.ResponseWriter, request *http.Request)  {
    err := request.ParseForm()  //必须在写响应内容之前调用
    fmt.Fprint(writer, pageTop, form)
    if err != nil {
        fmt.Fprintf(writer, anError, err)
    } else {
        if numbers, message, ok := processRequest(request); ok {
            
        }
    }
}

func getStats(numbers []float64) (stats statistics) {
    stats.numbers = numbers
    sort.Float64s(stats.numbers)  //对原数组升序排列
}

func sum(numbers []float64) (total float64) {
    for _, x := range numbers {
        total += x
    }
    return total
}

func mean(numbers []float64) float64 {
    return sum(numbers)/float64(len(numbers))
}

func median(numbers []float64) float64 {
    middle := len(numbers)/2
    result := numbers[middle]
    if len(numbers)%2 == 0 {
        result = (result + numbers[middle-1])/2
    }
    return result
}

