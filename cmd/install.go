package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

func init() {
	rootCmd.AddCommand(installCmd)
}

// Service is a docker-compose service in YAML
type Service struct {
	Name struct {
		Image         string
		ContainerName string `yaml:"container_name"`
		Environment   struct{}
		Volumes       struct{}
		Ports         struct{}
		Restart       string
	}
}

var installCmd = &cobra.Command{
	Use:   "install",
	Short: "Run the setup for home media server",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Home Media Server Setup")
	},
}
