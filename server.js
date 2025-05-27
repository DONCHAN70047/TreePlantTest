const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json({ limit: '20mb' }));


app.post('/get-link', (req, res) => {
  const { image } = req.body;

  if (!image) {
    return res.status(400).json({ error: 'No image received.' });
  }

  console.log(`Received image of length: ${image.length}`);

  const pythonProcess = spawn('python', ['server.py']);
  let result = '';
  let errorOutput = '';

  pythonProcess.stdin.on('error', (err) => {
    console.error('Error writing to Python stdin:', err);
    if (!res.headersSent) {
      res.status(500).json({ error: 'Error writing to Python stdin', details: err.message });
    }
  });

  pythonProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python script exited with code ${code}`);
      if (!res.headersSent) {
        return res.status(500).json({ error: "Python script failed.", details: errorOutput });
      }
    } else {
      console.log('Python script output:', result.trim());
      if (!res.headersSent) {
        res.json({ output: result.trim() });
      }
    }
  });

  pythonProcess.on('error', (err) => {
    console.error('Failed to start Python process:', err);
    if (!res.headersSent) {
      res.status(500).json({ error: "Failed to start Python process", details: err.message });
    }
  });

  pythonProcess.stdin.write(image);
  pythonProcess.stdin.end();
});


app.post('/confirmation', (req, res) => {
  const { image, confirmation } = req.body;

  console.log("User confirmed:", confirmation);


  res.json({
    output: confirmation
      ? "✅ Thank you! Your confirmation has been saved."
      : "❌ Thanks! Your feedback has been noted."
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
