package main

import (
	"log"
	"os"
	"os/user"
	"time"
)

func main() {
	switch os.Args[1] {
	case "help":
		log.Println("use with subcommands 'hello' or 'time'.")
	case "hello":
		user, err := user.Current()
		if err != nil {
			log.Fatalf("error fetching current user: %v", err)
		}
		log.Printf("Hello, %s\n", user.Username)
	case "time":
		now := time.Now()
		log.Printf("The time is %s\n", now.Local().String())
	}
}
