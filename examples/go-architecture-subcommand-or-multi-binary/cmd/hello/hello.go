package main

import (
	"log"
	"os/user"
)

func main() {
	user, err := user.Current()
	if err != nil {
		log.Fatalf("error fetching current user: %v", err)
	}
	log.Printf("Hello, %s\n", user.Username)
}
