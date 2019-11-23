package cmd

import (
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
		cmd.Println("Home Media Server Setup")
		cmd.Println()

		option := args[0]

		if option == "full" {
			cmd.Println("Installing the full Home Media Server with Sonarr, Radarr, Jackett, Transmission, and Plex")
			composeFile := Service{}
			cmd.Println(composeFile.Name)
			cmd.Println("testing")
		}
	},
}
