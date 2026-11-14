/**
 * Dispute Escalation Benchmark - Web Dashboard Server
 * Zero-dependency pure Node.js HTTP server.
 * Clones, builds, and runs in sterile CI/CD environments without any .env file.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const BASE_DIR = __dirname;

function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case '.html': return 'text/html; charset=utf-8';
    case '.css': return 'text/css';
    case '.js': return 'application/javascript';
    case '.json': return 'application/json';
    case '.svg': return 'image/svg+xml';
    case '.png': return 'image/png';
    case '.md': return 'text/markdown; charset=utf-8';
    default: return 'text/plain';
  }
}

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host}`);
  const pathname = parsedUrl.pathname;

  // API endpoints
  if (pathname === '/api/stats') {
    const statsPath = path.join(BASE_DIR, 'data', 'summary_statistics.json');
    if (fs.existsSync(statsPath)) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(fs.readFileSync(statsPath, 'utf8'));
    }
  }

  if (pathname === '/api/scenarios') {
    const scPath = path.join(BASE_DIR, 'data', 'scenarios.json');
    if (fs.existsSync(scPath)) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(fs.readFileSync(scPath, 'utf8'));
    }
  }

  if (pathname === '/api/results') {
    const resPath = path.join(BASE_DIR, 'data', 'benchmark_results.json');
    if (fs.existsSync(resPath)) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(fs.readFileSync(resPath, 'utf8'));
    }
  }

  // Static figures
  if (pathname.startsWith('/figures/')) {
    const figFile = path.basename(pathname);
    const figPath = path.join(BASE_DIR, 'figures', figFile);
    if (fs.existsSync(figPath)) {
      res.writeHead(200, { 'Content-Type': getMimeType(figPath) });
      return res.end(fs.readFileSync(figPath));
    }
  }

  // HTML Dashboard
  if (pathname === '/' || pathname === '/index.html') {
    const htmlPath = path.join(BASE_DIR, 'public', 'index.html');
    if (fs.existsSync(htmlPath)) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(fs.readFileSync(htmlPath, 'utf8'));
    }
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Not Found');
});

server.listen(PORT, () => {
  console.log(`Dispute Escalation Benchmark server running at http://localhost:${PORT}`);
  console.log(`Mode: Sterile Offline Fixture (Demo Mode Active)`);
});
