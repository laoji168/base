package bubblesort

import (
    "fmt"
    "testing"
)

func TestBubbleSort1(t *testing.T) {
    values := []int{5,4,3,2,1}
    BubbleSort(values)
    fmt.Println(values)
    for i:=0; i<len(values)-1; i++ {
        if values[i] > values[i+1] {
            t.Error("BubbleSort() faild. Got at ", values[i], values[i+1])
            break
        }
    }
}

func TestBubbleSort2(t *testing.T) {
    values := []int{5}
    BubbleSort(values)
    fmt.Println(values)
    if values[0] != 5 {
        t.Error("BubbleSort() faild. Got ", values, "Excepted 5")
    }
}
