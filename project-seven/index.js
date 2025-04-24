const http = require('http');
const fs = require('fs');
const url = require('url');
const { exec } = require('child_process');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);

  if (parsedUrl.pathname === '/' && req.method === 'GET') {
    fs.readFile('index.html', (err, data) => {
      if (err) {
        res.statusCode = 500;
        res.end('Error loading page');
      } else {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'text/html');
        res.end(data);
      }
    });
  } else if (parsedUrl.pathname === '/submit' && req.method === 'GET') {
    const ticker = parsedUrl.query.ticker;

    // Execute Python script with the ticker
    exec(`"C:\\Users\\rocca\\anaconda3\\python.exe" "C:\\Users\\rocca\\PycharmProjects\\pythonProjectSeven\\main.py" ${ticker}`, (error, stdout, stderr) => {
      if (error) {
        res.statusCode = 500;
        res.end(`Error: ${error.message}`);
        return;
      }
      if (stderr) {
        res.statusCode = 500;
        res.end(`stderr: ${stderr}`);
        return;
      }

      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/plain');
      res.end(stdout); // Output from Python script
    });
  } else {
    res.statusCode = 404;
    res.end('Not Found');
  }
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});