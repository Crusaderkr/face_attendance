const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Configure Multer for file upload
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const folderName = req.body.folderName;
        const folderPath = path.join(__dirname, 'uploads', folderName);
        createFolder(folderPath); // Create folder
        cb(null, folderPath);
    },
    filename: (req, file, cb) => {
        const ext = path.extname(file.originalname);
        cb(null, `${Date.now()}${ext}`); // Unique filename for uploaded file
    }
});
const upload = multer({ storage: storage });

// Serve index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Handle file upload
app.post('/upload', upload.single('image'), (req, res) => {
    res.send('Image uploaded successfully');
});

// Create uploads folder if it doesn't exist
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Function to create a folder if it doesn't exist
const createFolder = (folderPath) => {
    if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath);
        console.log(`Folder created: ${folderPath}`);
    }
};

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
