package app

import (
	"context"
	"log"
	"time"

	pb "github.com/ahnaf-zamil/stratus/deploy-node-agent/proto"
	"google.golang.org/protobuf/types/known/emptypb"

	"github.com/shirou/gopsutil/cpu"
	"github.com/shirou/gopsutil/mem"
)

type GRPCServer struct {
	pb.UnimplementedDeploymentNodeServer
	NODE_ID string
}

func (s *GRPCServer) HealthCheck(ctx context.Context, in *emptypb.Empty) (*pb.HealthCheckResponse, error) {
	/* Returns node CPU and memory usage */
	cpuPercentages, err := cpu.Percent(time.Second, false)
	if err != nil {
		return nil, err
	}

	memInfo, err := mem.VirtualMemory()
	if err != nil {
		return nil, err
	}

	return &pb.HealthCheckResponse{NodeId: s.NODE_ID, MemoryPerc: memInfo.UsedPercent, CpuPerc: cpuPercentages[0]}, nil
}

func (s *GRPCServer) DeployApp(ctx context.Context, in *pb.DeployAppRequest) (*pb.DeployAppResponse, error) {
	log.Println("Deploying", in.DeploymentId)

	// TODO: Download code from MinIO and create containers using Docker API
	return &pb.DeployAppResponse{Accepted: true}, nil
}
