package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
)

func init() {
	rootCmd.AddCommand(installCmd)
}

var installCmd = &cobra.Command{
	Use: "install",
	Short: "Run the setup for home media server",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Installing...")
	},
}
