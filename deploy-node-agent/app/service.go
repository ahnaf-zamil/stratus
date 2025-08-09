package app

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/ahnaf-zamil/stratus/deploy-node-agent/lib"
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
		log.Println(err)
		return nil, err
	}

	memInfo, err := mem.VirtualMemory()
	if err != nil {
		log.Println(err)
		return nil, err
	}

	return &pb.HealthCheckResponse{NodeId: s.NODE_ID, MemoryPerc: memInfo.UsedPercent, CpuPerc: cpuPercentages[0]}, nil
}

func (s *GRPCServer) DeployApp(ctx context.Context, in *pb.DeployAppRequest) (*pb.DeployAppResponse, error) {
	log.Println("Deploying", in.DeploymentId)

	filePath, err := lib.DownloadDeploymentZipFile(ctx, in.GetDeploymentId(), ZIP_FILE_OUTPUT_DIR)
	if err != nil {
		log.Println(err)
		return nil, err
	}

	homeDir, err := os.UserHomeDir()
	if err != nil {
		log.Println(err)
		return nil, err
	}

	deploymentFolder := fmt.Sprintf("%s/%s/%s", homeDir, "deployments", in.GetDeploymentId())

	err = os.MkdirAll(deploymentFolder, 0777)
	if err != nil {
		log.Println(err)
		return nil, err
	}

	err = lib.UnzipDeploymentZipFile(filePath, deploymentFolder)
	if err != nil {
		log.Println(err)
		return nil, err
	}
	// delete temp zip file, we can ignore any errors if they occur
	os.Remove(filePath)

	// TODO: Run deployment code in docker container

	return &pb.DeployAppResponse{Accepted: true}, nil
}
