package main

import (
	"log"
	"time"
)

func main() {
	now := time.Now()
	log.Printf("The time is %s\n", now.Local().String())
}
