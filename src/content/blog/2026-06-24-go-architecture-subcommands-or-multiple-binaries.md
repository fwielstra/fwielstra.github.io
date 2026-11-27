---
title: 'Go Architecture: Subcommands or multiple binaries?'
pubDate: 2026-06-24 13:37:00
description: When building software in Go that can do several distinct tasks, you have a number of options. In this post we'll discuss two and their pros and cons.
tags:
 - go
 - architecture
 - navara blog
---

*Note: This post was originally written for the internal engineering blog of my employer, Navara (part of BBTG), on June 24th, 2026; the published date of this repost has been backdated to match. The original is only available to colleagues, so it is not linked here.*

# Go Architecture: Subcommands or multiple binaries?

When building software in Go, often times the code has multiple distinct tasks it needs to execute. A server application may need to migrate a database, serve a HTTP based API, or export data; a command-line interface may need to perform several tasks, each task with its own set of flags and documentation.

In this post we'll discuss two of those, how to implement either, and the tradeoffs between the two.

The example source files are available in [the GitHub repository](https://github.com/fwielstra/fwielstra.github.io/tree/main/examples/go-architecture-subcommand-or-multi-binary).

## Subcommands

A subcommand is a common pattern in command-line interfaces, usually the first word after the main command. Each subcommand may have its own flags, or it can have flags shared with other subcommands. Subcommands can even have their own subcommands and flags again. Some examples:

* `git commit`
* `git add`
* `npm install`
* `gh auth login`
* `docker login -u <username>`

In practice, this means that your application is distributed as a single, "big" binary that contains all the code and dependencies needed to execute all of the subcommands.

This can be written by hand, for example:

```go
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
```

However, this is a very basic example; a well-formed CLI needs to gracefully handle invalid input, [provide help](https://clig.dev/#help) and documentation, etc. While all of this can be coded by hand, you can also use a 3rd party library like [spf13/cobra](https://github.com/spf13/cobra) to write your command-line interface declaratively. For example:

```go
package main

import (
	"log"
	"os/user"
	"time"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "cobracli",
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
```

A CLI written with Cobra will automatically generate documentation on the available subcommands and flags, and it can output readable errors when unsupported subcommands or flags are passed.

## Multiple binaries

An alternative to having a single binary with different subcommands is to build multiple binaries. In a Go codebase, you can create multiple binaries by putting a `package main` in several subfolders:

```text
.
├── bin
│   ├── hello
│   ├── time
│   └── serve
├── cmd
│   ├── hello
│   │   └── hello.go
│   ├── time
│   │   └── time.go
│   └── serve
│       └── serve.go
├── go.mod
├── go.sum
├── LICENSE
└── README.md
```

When running `go build -o bin ./cmd/...`, each `main` package within the `cmd` subfolder will result in its own discrete binary, named after the folder it lives in.

(note that the filename is arbitrary, you can also name each of them `main.go`)

## Tradeoffs

One of the most important distinctions between the two approaches is the size of the resulting binary and dependency isolation. When using the multiple binaries approach, the Go compiler will only include the code and libraries used by the individual main packages; in the above example, the `serve` binary could rely on a 3rd party HTTP server library, which would not be included in the `hello` and `time` binaries.

This is a great approach for when you need your binaries to be small, for example when they're deployed in lambda or edge computing environments.

The subcommand approach allows you to create a single but versatile binary, which is ideal for discoverability - run e.g. `docker help` and you will get a list of all available features. It also simplifies release management, especially when you distribute your binary for multiple platforms and architectures.

Use subcomands when size matters less, when discoverability matters, when configuration is shared and you want to offer a unified CLI experience. Use multiple binaries when the commands and code paths are independent, when binary size matters, and when dependency isolation is important.

## Further Reading

* [clig.dev, an extensive guide for writing command-line interfaces](https://clig.dev/)
* [The 12-Factor App](https://12factor.net/)
* [Minimize the size of your Go binary](https://www.codestudy.net/blog/how-to-reduce-go-compiled-file-size/)
* [Command-Line Interfaces on the official go.dev documentation](https://go.dev/solutions/clis)
* [Subcommand example: the Github CLI](https://github.com/cli/cli)
* [Subcommand example: the Docker CLI](https://github.com/docker/cli)
* [Multiple binaries example: Kubernetes](https://github.com/kubernetes/kubernetes/)
* [Multiple binaries example: Ethereum](https://github.com/ethereum/go-ethereum)

## AI disclosure

No AI was used in writing this post or its examples.
