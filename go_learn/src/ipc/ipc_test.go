package ipc

import (
    "testing"
)

type EchoServer struct {
}

func (server * EchoServer) Handle(request string) string {
    return "ECHO:" + request
}

func (server * EchoServer) Name() string {
    return "EchoServer"
}

func TestIpc (t * testing.T) {
    server := NewIpcServer(&EchoServer{})

    client1 := NewIpcClient(server)
    client2 := NewIpcClient(server)

    resq1 := client1.Call("From client1")
    resq2 := client1.Call("From client2")

    if resp1 != "ECHO:From client1" || resp2 != "ECHO:From client2" {
        t.Error("IpcClient.Call faild. resp1:", resp1, "resp2:", resp2)
    }
    client1.Close()
    client2.Close()
}