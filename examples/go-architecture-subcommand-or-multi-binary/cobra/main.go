package main

import (
	"log"
	"os/user"
	"time"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "hello",
	Short: "A brief description of your application",
	Long: `A longer description that spans multiple lines and likely contains
examples and usage of using your application.`,
}

var helloCmd = &cobra.Command{
	Use:   "hello",
	Short: "Print a friendly greeting",
	Args:  cobra.MaximumNArgs(0),
	RunE: func(cmd *cobra.Command, args []string) error {
		user, err := user.Current()
		if err != nil {
			return err
		}
		log.Printf("Hello, %s\n", user.Username)
		return nil
	},
}

var timeCmd = &cobra.Command{
	Use:   "time",
	Short: "Print the current time",
	Args:  cobra.MaximumNArgs(0),
	Run: func(cmd *cobra.Command, args []string) {
		now := time.Now()
		log.Printf("The time is %s\n", now.Local().String())
	},
}

func main() {
	rootCmd.AddCommand(helloCmd)
	rootCmd.AddCommand(timeCmd)

	err := rootCmd.Execute()
	if err != nil {
		log.Fatalf("error running command: %v", err)
	}
}
