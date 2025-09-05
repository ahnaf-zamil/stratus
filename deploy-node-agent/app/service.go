package app

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/ahnaf-zamil/stratus/deploy-node-agent/lib"
	"github.com/ahnaf-zamil/stratus/deploy-node-agent/util"
	pb "github.com/ahnaf-zamil/stratus/shared/proto_go"
	"google.golang.org/protobuf/types/known/emptypb"

	"github.com/shirou/gopsutil/cpu"
	"github.com/shirou/gopsutil/mem"
)

// GRPCServer implements the DeploymentNode gRPC service.
// It runs on each deployment node and handles health checks and deployment requests.
type GRPCServer struct {
	pb.UnimplementedDeploymentNodeServer
	NODE_ID string // Unique identifier for this node, returned in health checks
}

// HealthCheck returns the current CPU and memory usage of the node.
// This is used by the management plane to determine node load.
func (s *GRPCServer) HealthCheck(ctx context.Context, in *emptypb.Empty) (*pb.HealthCheckResponse, error) {
	// Sample CPU usage over 1 second
	cpuPercentages, err := cpu.Percent(time.Second, false)
	if err != nil {
		log.Println("CPU sampling error:", err)
		return nil, err
	}

	// Get memory usage stats
	memInfo, err := mem.VirtualMemory()
	if err != nil {
		log.Println("Memory sampling error:", err)
		return nil, err
	}

	// Return usage metrics along with node ID
	return &pb.HealthCheckResponse{
		NodeId:     s.NODE_ID,
		MemoryPerc: memInfo.UsedPercent,
		CpuPerc:    cpuPercentages[0],
	}, nil
}

// DeployApp handles a deployment request from the management plane.
// It downloads the deployment artifact, unpacks it, and launches the container.
// The task runs asynchronously to avoid blocking the gRPC thread.
func (s *GRPCServer) DeployApp(ctx context.Context, in *pb.DeployAppRequest) (*pb.DeployAppResponse, error) {
	log.Println("Deploying", in.DeploymentId)

	// Run deployment in a background goroutine
	go func() {
		err := func() error {
			ctx := context.TODO() // Use a fresh context for internal operations

			// Download the deployment zip file from MinIO
			filePath, err := lib.DownloadDeploymentZipFile(ctx, in.GetDeploymentId(), util.ZIP_FILE_OUTPUT_DIR)
			if err != nil {
				return fmt.Errorf("failed to download zip: %w", err)
			}

			// Get the home directory to store unpacked deployments
			homeDir, err := os.UserHomeDir()
			if err != nil {
				return fmt.Errorf("failed to get home dir: %w", err)
			}

			// Create a unique folder for this deployment
			deploymentFolder := fmt.Sprintf("%s/deployments/%s", homeDir, in.GetDeploymentId())
			err = os.MkdirAll(deploymentFolder, 0777)
			if err != nil {
				return fmt.Errorf("failed to create deployment folder: %w", err)
			}

			// Unzip the deployment artifact into the folder
			err = lib.UnzipDeploymentZipFile(filePath, deploymentFolder)
			if err != nil {
				return fmt.Errorf("failed to unzip deployment: %w", err)
			}

			// Clean up the temporary zip file (ignore errors)
			_ = os.Remove(filePath)

			// Launch the container using the unpacked code
			err = lib.RunDeploymentContainer(ctx, in.GetDeploymentId(), deploymentFolder)
			if err != nil {
				return fmt.Errorf("failed to run container: %w", err)
			}

			return nil
		}()

		if err != nil {
			// TODO: Report deployment failure to management plane or log persistently
			log.Println("Deployment error:", err)
			return
		}

		log.Printf("Successfully created deployment %s\n", in.GetDeploymentId())
	}()

	// Immediately return an accepted response to the management plane
	return &pb.DeployAppResponse{Accepted: true}, nil
}
