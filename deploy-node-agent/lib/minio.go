package lib

/*

 */

import (
	"archive/zip"
	"context"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

var MINIO_HOST = "127.0.0.1:9000"
var MINIO_ACCESS_KEY = "admin"
var MINIO_SECRET_KEY = "admin123"
var USE_SSL = false // for now

var DEPLOY_BUCKET = "stratus-deployments"

var minioClient *minio.Client

func GetMinIOClient() (*minio.Client, error) {
	if minioClient != nil {
		return minioClient, nil
	}

	minioClient, err := minio.New(MINIO_HOST, &minio.Options{
		Creds:  credentials.NewStaticV4(MINIO_ACCESS_KEY, MINIO_SECRET_KEY, ""),
		Secure: USE_SSL,
	})

	return minioClient, err
}

func DownloadDeploymentZipFile(ctx context.Context, deployment_id string, output_dir string) (string, error) {
	client, err := GetMinIOClient()
	if err != nil {
		return "", err
	}

	fileName := fmt.Sprintf("%s.zip", deployment_id)
	download_path := fmt.Sprintf("/tmp/%s", fileName)

	return download_path, client.FGetObject(context.Background(), DEPLOY_BUCKET, fileName, download_path, minio.GetObjectOptions{})
}

func UnzipDeploymentZipFile(filePath string, outputParentDir string) error {
	reader, err := zip.OpenReader(filePath)
	if err != nil {
		return err
	}
	defer reader.Close()

	for _, f := range reader.File {
		newFilePath := fmt.Sprintf("%s/%s", outputParentDir, f.Name)

		// Prevent Zip Slip vulnerability
		if !strings.HasPrefix(filepath.Clean(newFilePath), filepath.Clean(outputParentDir)+string(os.PathSeparator)) {
			return fmt.Errorf("illegal file path: %s", newFilePath)
		}

		if f.FileInfo().IsDir() {
			// Create directory
			if err := os.MkdirAll(newFilePath, os.ModePerm); err != nil {
				return err
			}
			continue
		}

		// Ensure parent directories exist
		if err := os.MkdirAll(filepath.Dir(newFilePath), os.ModePerm); err != nil {
			return err
		}

		// Create file
		rc, err := f.Open()
		if err != nil {
			return err
		}
		defer rc.Close()

		outFile, err := os.Create(newFilePath)
		if err != nil {
			return err
		}
		defer outFile.Close()

		if _, err := io.Copy(outFile, rc); err != nil {
			return err
		}
	}

	return nil
}
