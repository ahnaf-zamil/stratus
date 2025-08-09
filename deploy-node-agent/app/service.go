package app

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/ahnaf-zamil/stratus/deploy-node-agent/lib"
	pb "github.com/ahnaf-zamil/stratus/deploy-node-agent/proto"
	"github.com/ahnaf-zamil/stratus/deploy-node-agent/util"
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

	// Create background deployment task and immediately return an Accepted response
	go func() {
		err := func() error {
			ctx := context.TODO()

			filePath, err := lib.DownloadDeploymentZipFile(ctx, in.GetDeploymentId(), util.ZIP_FILE_OUTPUT_DIR)
			if err != nil {
				return err
			}

			homeDir, err := os.UserHomeDir()
			if err != nil {
				return err
			}

			deploymentFolder := fmt.Sprintf("%s/%s/%s", homeDir, "deployments", in.GetDeploymentId())

			err = os.MkdirAll(deploymentFolder, 0777)
			if err != nil {
				return err
			}

			err = lib.UnzipDeploymentZipFile(filePath, deploymentFolder)
			if err != nil {
				return err
			}
			// delete temp zip file, we can ignore any errors if they occur
			os.Remove(filePath)

			// Run the container!
			err = lib.RunDeploymentContainer(ctx, in.GetDeploymentId(), deploymentFolder)
			if err != nil {
				return err
			}
			return nil
		}()

		if err != nil {
			// TODO: Handle errors. Maybe trigger a deployment failure or log it somewhere
			log.Println(err)
			return
		}

		log.Printf("Successfully created deployment %s\n", in.GetDeploymentId())
	}()

	return &pb.DeployAppResponse{Accepted: true}, nil
}
