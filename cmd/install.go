package cmd

import (
	"github.com/danielfain/home-media-server/model"
	"github.com/spf13/cobra"
)

func init() {
	rootCmd.AddCommand(installCmd)
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
			composeFile := model.Service{}
			cmd.Println(composeFile)
			cmd.Println("testing")
		}
	},
}
