//qsort_test.go
package qsort

import (
    "fmt"
    "testing"
)

func TestQuickSort1(t * testing.T) {
    values := []int {5, 4, 3, 2, 1}
    QuickSort(values)
    fmt.Println(values)
    var i int;
    var j int = len(values) - 1
    for i = 0; i < j; i++ {
        if values[i] > values[i + 1] {
            t.Error("QuickSort() faild")
            break;
        }
    }
}

func TestQuickSort2(t * testing.T) {
    values := []int {5}
    QuickSort(values)
    fmt.Println(values)
    if values[0] != 5 {
        t.Error("QuickSort() faild. Got", values);
    }
}
