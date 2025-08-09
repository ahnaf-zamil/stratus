package main

import (
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"

	"github.com/ahnaf-zamil/stratus/deploy-node-agent/app"
	"github.com/ahnaf-zamil/stratus/deploy-node-agent/lib"
	"github.com/ahnaf-zamil/stratus/deploy-node-agent/util"
	"github.com/ahnaf-zamil/stratus/shared/proto_go"
)

var port int = 6969
var host string = "0.0.0.0"

func main() {
	host_str := fmt.Sprintf("%s:%d", host, port)
	lis, err := net.Listen("tcp", host_str)

	if err != nil {
		log.Fatalf("failed to listen on %s: %v", host_str, err)
	}
	gServer := &app.GRPCServer{NODE_ID: util.GenerateCryptoID()}
	s := grpc.NewServer()
	proto_go.RegisterDeploymentNodeServer(s, gServer)

	defer lib.CleanupDockerClient()

	log.Printf("Stratus Deployment Node Agent listening on %v", lis.Addr())
	log.Printf("Node ID:	%v", gServer.NODE_ID)

	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve : %v", err)
	}
}
