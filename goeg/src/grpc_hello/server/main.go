package main

import (
    "golang.org/x/net/context"
    "google.golang.org/grpc"
    pd "grpc_hello"
    "log"
    "net"
)

const (
    port = ":50051"
)

// server is used to implement helloworld.GreeterServer.
type server struct{}

// SayHello implements helloworld.GreeterServer
func (s *server) SayHello(ctx context.Context, in *pd.HelloRequest) (*pd.HelloReply, error) {
    log.Printf("received: %v", in.Name)
    return &pd.HelloReply{Message:"hello" + in.Name}, nil
}

func main() {
    lis, err := net.Listen("tcp", port)
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }

    s := grpc.NewServer()
    pd.RegisterGreeterServer(s, &server{})
    if err := s.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}