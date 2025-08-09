package lib

import (
	"context"
	"fmt"

	"github.com/ahnaf-zamil/stratus/deploy-node-agent/util"
	"github.com/moby/moby/api/types/container"
	"github.com/moby/moby/api/types/mount"
	"github.com/moby/moby/client"
)

var apiClient *client.Client

const (
	ContainerImagePython = "stratus_test:latest"
)

func intPtr(i int64) *int64 {
	return &i
}

func getAPIClient() (*client.Client, error) {
	if apiClient != nil {
		return apiClient, nil
	}
	apiClient, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	return apiClient, err
}

func RunDeploymentContainer(ctx context.Context, deploymentId string, deploymentFilesPath string) error {
	// TODO: Check if any other containers exist for this deployment or not

	client, err := getAPIClient()
	if err != nil {
		return err
	}
	// Generate a logical container ID. We'll use this in the application instead of the Docker generated one
	containerId := util.GenerateCryptoID()

	config := &container.Config{
		Image: ContainerImagePython,
		Labels: map[string]string{
			"deployment-id":        deploymentId,
			"logical-container-id": containerId,
		},
		Env: []string{
			// Some env vars for the container
			fmt.Sprintf("DEPLOYMENT_ID=%s", deploymentId),
			fmt.Sprintf("LOGICAL_CONTAINER_ID=%s", containerId),
		},
	}

	hostConfig := &container.HostConfig{
		// This is important, make sure we be using gvisor
		Runtime:     "runsc",
		SecurityOpt: []string{"apparmor=gvisor-profile"},
		Mounts: []mount.Mount{
			{
				Type:     mount.TypeBind,
				Source:   deploymentFilesPath,
				Target:   "/app",
				ReadOnly: false,
			},
		},
		// may change this later
		Resources: container.Resources{
			Memory:    256 * 1024 * 1024, // 256 mb
			CPUQuota:  50000,             // 0.5 of a cpu
			PidsLimit: intPtr(100),
		},
	}

	resp, err := client.ContainerCreate(ctx, config, hostConfig, nil, nil, fmt.Sprintf("deploy-%s-%s", deploymentId, containerId))
	if err != nil {
		return err
	}

	// Start the container
	if err := client.ContainerStart(ctx, resp.ID, container.StartOptions{}); err != nil {
		return err
	}

	return nil
}

func CleanupDockerClient() {
	if apiClient != nil {
		apiClient.Close()
	}
}
