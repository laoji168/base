package main

import (
    "os"
    "testing"
)

func TestAdd(t *testing.T) {
    var tests = []struct{
        x int
        y int
        expect int
    } {
        {1, 1, 2},
        {2, 2, 4},
        {3, 2, 5},
    }

    for _, tt := range tests{
        actual := add(tt.x, tt.y)
        if actual != tt.expect {
            t.Errorf("add(%d, %d): expect %d, actual %d", tt.x, tt.y, tt.expect, actual)
        }
    }
}

func BenchmarkAdd(b *testing.B) {
    b.ReportAllocs()
    b.ResetTimer()
    for i:=0;i<b.N;i++ {
        _ = add(1,2)
    }
}

func TestMain(m *testing.M) {
    // setup
    code := m.Run()  //调用测试用例
    // teardown
    os.Exit(code)  //os.Exit 不会执行defer

}
