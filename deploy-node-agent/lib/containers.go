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

// Helper to get pointer to int64 (used in resource limits)
func intPtr(i int64) *int64 {
	return &i
}

// Lazily initializes and returns a Docker API client
func getAPIClient() (*client.Client, error) {
	if apiClient != nil {
		return apiClient, nil
	}
	apiClient, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	return apiClient, err
}

// RunDeploymentContainer launches a container for the given deployment ID.
// It mounts the deployment code, applies resource limits, and uses gVisor for isolation.
func RunDeploymentContainer(ctx context.Context, deploymentId string, deploymentFilesPath string) error {
	// TODO: Check if any other containers exist for this deployment or not

	client, err := getAPIClient()
	if err != nil {
		return err
	}

	// Generate a logical container ID for internal tracking
	containerId := util.GenerateCryptoID()

	config := &container.Config{
		Image: ContainerImagePython,
		Labels: map[string]string{
			"deployment-id":        deploymentId,
			"logical-container-id": containerId,
		},
		Env: []string{
			fmt.Sprintf("DEPLOYMENT_ID=%s", deploymentId),
			fmt.Sprintf("LOGICAL_CONTAINER_ID=%s", containerId),
		},
	}

	hostConfig := &container.HostConfig{
		// gVisor runtime with DNS override for outbound resolution
		DNS:         []string{"1.1.1.1"},
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
		Resources: container.Resources{
			Memory:    256 * 1024 * 1024,
			CPUQuota:  50000,
			PidsLimit: intPtr(100),
		},
	}

	// Create container with deterministic name
	resp, err := client.ContainerCreate(ctx, config, hostConfig, nil, nil, fmt.Sprintf("deploy-%s-%s", deploymentId, containerId))
	if err != nil {
		return err
	}

	// Start container
	if err := client.ContainerStart(ctx, resp.ID, container.StartOptions{}); err != nil {
		return err
	}

	return nil
}

// CleanupDockerClient closes the Docker API client if initialized
func CleanupDockerClient() {
	if apiClient != nil {
		apiClient.Close()
	}
}
