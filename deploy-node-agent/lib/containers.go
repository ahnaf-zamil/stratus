package lib

import (
	"github.com/moby/moby/client"
)

var apiClient *client.Client

func getAPIClient() (*client.Client, error) {
	if apiClient != nil {
		return apiClient, nil
	}
	apiClient, err := client.NewClientWithOpts(client.FromEnv)
	return apiClient, err
}
